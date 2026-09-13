import os
import sys
import re
import time
import math
import threading
import tempfile
import numpy as np
import scipy.io.wavfile as wav
import sounddevice as sd
import keyboard
import pyperclip
import pyautogui
import tkinter as tk
from faster_whisper import WhisperModel

SAMPLE_RATE = 16000
BLOCK_SIZE = 512  # Ultra-low latency sample frame buffer

# --- Fast Local Whisper Engine ---
model = WhisperModel('tiny.en', device='cpu', compute_type='int8')

# --- Audio & App State ---
is_recording = False
is_processing = False
audio_buffer = []

smoothed_audio_level = 0.0
smoothed_audio_freq = 0.0

LOWER_DB = -58.0
UPPER_DB = 0.0

# --- Smart Trailing Punctuation Engine ---
def matches_pattern(text: str, pattern: str) -> bool:
    return bool(re.search(pattern, text, re.IGNORECASE))

def is_number(text: str) -> bool:
    return matches_pattern(text, r"^\+?\(?\d(?:[\d\s.,\-()/:]*\d)?$")

def is_email(text: str) -> bool:
    return matches_pattern(text, r"^[^\s@]+@[^\s@]+\.[^\s@]+$")

def is_url(text: str) -> bool:
    return matches_pattern(
        text,
        r"^(?:[a-z][a-z0-9+.\-]*://\S+|www\.\S+\.\S+|[a-z0-9\-]+(?:\.[a-z0-9\-]+)*\.[a-z]{2,}(?:[/:?#]\S*)?)$"
    )

def is_plain_token(text: str) -> bool:
    return bool(text) and not any(c.isspace() for c in text) and ("." not in text)

def smart_trailing_punctuation_strip(text: str) -> str:
    trimmed = text.strip()
    if not trimmed.endswith(".") or trimmed.endswith(".."):
        return text

    candidate = trimmed[:-1]
    if not candidate:
        return text

    if is_number(candidate) or is_email(candidate) or is_url(candidate) or is_plain_token(candidate):
        return candidate
    return text

# --- Transcription Normalizer Engine ---
PLACEHOLDER_PATTERNS = [
    r'\[(?:BLANK_AUDIO|SILENCE)\]',
    r'<\|nospeech\|>',
    r'\[\s*S\s*\]'
]

NOISE_TERMS = [
    "applause", "background noise", "blank audio", "breathing", "cough",
    "coughing", "exhale", "heartbeat", "indistinct", "inaudible", "inhale",
    "laughing", "laughter", "loud noise", "muffled speech", "music", "noise",
    "silence", "sigh", "sighs", "sniffing", "static", "unclear speech",
    "unintelligible", "wind", "wind blowing", "wind noise"
]
NOISE_REGEX = re.compile(r'[\[\(]\s*(?:' + '|'.join(map(re.escape, NOISE_TERMS)) + r')\s*[\]\)]', re.IGNORECASE)
FILLER_REGEX = re.compile(r'(?i)(^|[\s,.;:!?])(?:uh+|um+|umm+|uhm+|erm+|hmm+)(?=$|[\s,.;:!?])[,.;:!?]?')

def normalize_transcription(text: str) -> str:
    for pattern in PLACEHOLDER_PATTERNS:
        text = re.sub(pattern, ' ', text)
    text = NOISE_REGEX.sub(' ', text)
    text = FILLER_REGEX.sub(r'\1', text)
    text = re.sub(r'\s+([,.;:!?])', r'\1', text)
    text = re.sub(r'\s+', ' ', text)
    clean_text = text.strip()
    return smart_trailing_punctuation_strip(clean_text)

# --- Floating Stadium Pill UI ---
root = tk.Tk()
root.withdraw()
root.overrideredirect(True)
root.attributes('-topmost', True)

CHROMA_KEY = '#000001'
root.config(bg=CHROMA_KEY)
root.wm_attributes('-transparentcolor', CHROMA_KEY)

WIDTH = 142
HEIGHT = 44
RADIUS = HEIGHT // 2

canvas = tk.Canvas(root, width=WIDTH, height=HEIGHT, bg=CHROMA_KEY, highlightthickness=0)
canvas.pack()

def position_window():
    root.update_idletasks()
    sw = root.winfo_screenwidth()
    sh = root.winfo_screenheight()
    x = (sw // 2) - (WIDTH // 2)
    y = sh - HEIGHT - 75
    root.geometry(f'{WIDTH}x{HEIGHT}+{x}+{y}')

def draw_pill_container(bg='#161B22', border='#30363D'):
    canvas.delete('all')
    canvas.create_oval(0, 0, HEIGHT, HEIGHT, fill=bg, outline=border, width=1.5)
    canvas.create_oval(WIDTH - HEIGHT, 0, WIDTH, HEIGHT, fill=bg, outline=border, width=1.5)
    canvas.create_rectangle(RADIUS, 0, WIDTH - RADIUS, HEIGHT, fill=bg, outline='')
    canvas.create_line(RADIUS, 1, WIDTH - RADIUS, 1, fill=border, width=1.5)
    canvas.create_line(RADIUS, HEIGHT - 1, WIDTH - RADIUS, HEIGHT - 1, fill=border, width=1.5)

def draw_capsule_bar(cx, cy, half_w, half_h, color):
    canvas.create_oval(cx - half_w, cy - half_h, cx + half_w, cy - half_h + (2 * half_w), fill=color, outline='')
    canvas.create_oval(cx - half_w, cy + half_h - (2 * half_w), cx + half_w, cy + half_h, fill=color, outline='')
    canvas.create_rectangle(cx - half_w, cy - half_h + half_w, cx + half_w, cy + half_h - half_w, fill=color, outline='')

def animate_voice_hud():
    if not is_recording:
        return

    draw_pill_container(bg='#161B22', border='#30363D')

    bar_centers = [46, 62, 78, 94]
    palette = ['#1D4ED8', '#2563EB', '#38BDF8', '#67E8F9']
    cy = HEIGHT // 2
    t = time.time() * 12.0

    amp = smoothed_audio_level

    for i, cx in enumerate(bar_centers):
        wave_motion = math.sin(t + (i * 0.95)) * 0.25
        voice_factor = max(amp + (wave_motion * amp), 0.0)

        half_w = 3.2
        min_half_h = 3.2
        max_half_h = 13.5
        bar_h = min_half_h + ((max_half_h - min_half_h) * voice_factor)

        draw_capsule_bar(cx, cy, half_w, bar_h, palette[i])

    root.after(16, animate_voice_hud)

def show_transcribing():
    draw_pill_container(bg='#161B22', border='#30363D')
    canvas.create_text(WIDTH // 2, HEIGHT // 2, text='⚡ Transcribing', fill='#38BDF8', font=('Segoe UI', 9, 'bold'))
    root.deiconify()

# --- Audio Capture & Decibel DSP ---
def audio_callback(indata, frames, time_info, status):
    global audio_buffer, smoothed_audio_level, smoothed_audio_freq
    if not is_recording:
        return

    audio_buffer.append(indata.copy())

    samples = indata[:, 0]
    peak_level = float(np.max(np.abs(samples)))
    rms = float(np.sqrt(np.mean(samples**2)))

    db = 20.0 * math.log10(rms if rms > 0 else 0.0001)
    peak_db = 20.0 * math.log10(peak_level if peak_level > 0 else 0.0001)

    clamped_rms = max(LOWER_DB, min(UPPER_DB, db))
    clamped_peak = max(LOWER_DB, min(UPPER_DB, peak_db))

    norm_rms = (clamped_rms - LOWER_DB) / (UPPER_DB - LOWER_DB)
    norm_peak = (clamped_peak - LOWER_DB) / (UPPER_DB - LOWER_DB)
    norm_level = max(norm_rms * 0.8, norm_peak)

    if norm_level < 0.015:
        norm_level = 0.0

    smoothing = 0.55 if norm_level > smoothed_audio_level else 0.18
    smoothed_audio_level += (norm_level - smoothed_audio_level) * smoothing

# --- Clipboard Snapshot & Restore Pipeline ---
def process_and_paste(audio_data):
    global is_processing
    root.after(0, show_transcribing)

    # 1. Snapshot previous clipboard content
    previous_clipboard = None
    try:
        previous_clipboard = pyperclip.paste()
    except Exception:
        pass

    with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as tmp:
        wav.write(tmp.name, SAMPLE_RATE, (audio_data * 32767).astype(np.int16))
        tmp_path = tmp.name

    try:
        segments, _ = model.transcribe(
            tmp_path,
            beam_size=1,
            best_of=1,
            temperature=0.0,
            condition_on_previous_text=False
        )
        raw_text = ' '.join([seg.text.strip() for seg in segments]).strip()
        final_text = normalize_transcription(raw_text)

        if final_text:
            # 2. Paste new dictated text
            pyperclip.copy(final_text + ' ')
            time.sleep(0.05)
            pyautogui.hotkey('ctrl', 'v')

            # 3. Restore previous clipboard snapshot
            if previous_clipboard is not None:
                time.sleep(0.35)
                try:
                    if pyperclip.paste() == (final_text + ' '):
                        pyperclip.copy(previous_clipboard)
                except Exception:
                    pass
    except Exception:
        pass
    finally:
        if os.path.exists(tmp_path):
            os.remove(tmp_path)
        is_processing = False
        root.after(0, root.withdraw)

def start_recording():
    global is_recording, audio_buffer, is_processing, smoothed_audio_level
    if is_processing or is_recording:
        return

    audio_buffer = []
    smoothed_audio_level = 0.0
    is_recording = True
    position_window()
    root.deiconify()
    animate_voice_hud()

def stop_and_paste():
    global is_recording, audio_buffer, is_processing
    if not is_recording or is_processing:
        return

    is_recording = False
    is_processing = True

    if audio_buffer:
        audio_data = np.concatenate(audio_buffer, axis=0)
        threading.Thread(target=process_and_paste, args=(audio_data,), daemon=True).start()
    else:
        is_processing = False
        root.after(0, root.withdraw)

# Register Hotkeys
keyboard.add_hotkey('ctrl+space', start_recording)
keyboard.add_hotkey('enter', stop_and_paste)

# Audio Input Stream
stream = sd.InputStream(samplerate=SAMPLE_RATE, channels=1, blocksize=BLOCK_SIZE, callback=audio_callback)
stream.start()

root.mainloop()