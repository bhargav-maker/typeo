# 🎤 WhisperFlow - Voice-to-Text Typing Assistant

A lightweight, real-time speech-to-text application that converts your voice directly into text using **OpenAI's Whisper** (via faster-whisper). Simply press a hotkey, speak, and your words are automatically typed into any application. Perfect for hands-free typing, accessibility, and productivity.

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://python.org)
[![Whisper](https://img.shields.io/badge/Whisper-OpenAI-green.svg)](https://openai.com/research/whisper)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

**Topics:** Speech-to-Text • Voice Recognition • Whisper AI • Audio Processing • Accessibility • Productivity • Python • Real-time Transcription

---

## 📋 Table of Contents

- [Features](#-features)
- [System Requirements](#-system-requirements)
- [Installation](#-installation)
- [Quick Start](#-quick-start)
- [Hotkeys & Controls](#-hotkeys--controls)
- [Setup & Configuration](#-setup--configuration)
- [Windows Startup Setup](#-windows-startup-setup)
- [Troubleshooting](#-troubleshooting)
- [How It Works](#-how-it-works)
- [License](#-license)

---

## ✨ Features

### 🎙️ Voice Recognition
- **Real-time Transcription**: Instant speech-to-text conversion
- **Local Processing**: All processing happens on your computer (no cloud)
- **Whisper AI**: OpenAI's state-of-the-art speech recognition model
- **Multi-Language Support**: Supports 99+ languages (multilingual model available)

### 💻 Smart Text Integration
- **Auto-Typing**: Automatically types transcribed text into any application
- **Smart Punctuation**: Intelligently handles punctuation detection
- **Noise Filtering**: Removes filler words (um, uh, hmm) and background noise
- **Clipboard Preservation**: Restores your clipboard after pasting

### 🎨 User Interface
- **Floating Pill UI**: Minimalist floating indicator showing recording status
- **Real-time Audio Visualization**: Animated bars showing voice level
- **Transcription Indicator**: Visual feedback during processing
- **Dark Theme**: Modern, eye-friendly dark interface

### ⚡ Performance
- **Low Latency**: Ultra-fast audio processing (512 sample frame buffer)
- **CPU Optimized**: Runs efficiently on standard computers
- **Background Mode**: Works while you use other applications
- **Minimal Overhead**: Lightweight 142x44px floating UI

---

## 🖥️ System Requirements

### Minimum Requirements
| Component | Requirement |
|-----------|------------|
| **OS** | Windows 10/11, macOS 10.14+, Linux (Ubuntu 18.04+) |
| **Python** | 3.8 or higher |
| **RAM** | 2 GB minimum |
| **Disk Space** | 1 GB (for Whisper model) |
| **Microphone** | Any USB or built-in microphone |
| **Processor** | Intel i3 / AMD equivalent or better |

### Recommended Requirements
| Component | Recommendation |
|-----------|------------|
| **OS** | Windows 11 or latest macOS |
| **Python** | 3.10+ |
| **RAM** | 4+ GB |
| **Disk Space** | 2 GB (for optimal model variants) |
| **Microphone** | External USB microphone (better quality) |
| **Processor** | Intel i5/i7 or AMD Ryzen 5+ (faster transcription) |

---

## 💾 Installation

### Step 1: Clone the Repository
```bash
git clone https://github.com/bhargav-maker/typeo.git
cd typeo
```

### Step 2: Create Virtual Environment (Recommended)
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

**What each dependency does:**
- **numpy** (≥1.24.0) - Numerical computing for audio processing
- **scipy** (≥1.10.0) - Scientific functions for WAV file writing
- **sounddevice** (≥0.4.5) - Real-time audio input stream
- **keyboard** (≥0.13.5) - Hotkey binding and detection
- **pyperclip** (≥1.8.2) - Clipboard read/write operations
- **pyautogui** (≥0.9.54) - GUI automation (simulates typing)
- **faster-whisper** (≥0.10.0) - Fast, optimized speech-to-text engine

### Step 4: Download Whisper Model (First Run)
The application automatically downloads the Whisper model on first run:

```bash
# Run the application (will download ~1.5 GB model)
python whisperflow.pyw
```

**Model sizes available:**
- **tiny.en** (~40 MB) - Fastest, English only - DEFAULT
- **base.en** (~140 MB) - Balanced, English only
- **small.en** (~466 MB) - Better accuracy, English only
- **medium.en** (~1.5 GB) - High accuracy, English only
- **tiny** (~40 MB) - Fastest, multilingual
- **base** (~140 MB) - Balanced, multilingual
- **small** (~466 MB) - Better accuracy, multilingual

To use a different model, edit `whisperflow.pyw` line 21:
```python
model = WhisperModel('tiny.en', device='cpu', compute_type='int8')
#                      ^^^^^^^ - Change this to desired model
```

---

## 🚀 Quick Start

### Run WhisperFlow
```bash
python whisperflow.pyw
```

### Use It
1. **Start Recording**: Press `Ctrl + Space`
2. **Speak Clearly**: Talk into your microphone
3. **Stop Recording**: Press `Enter`
4. **Auto-Type**: Your speech is automatically typed into the active application

### Visual Indicators
- **Animated Bars** 🔵 - Recording in progress (shows voice level)
- **⚡ Transcribing** - Processing your speech
- **Floating Pill** - Minimalist UI that stays on top

---

## 🎹 Hotkeys & Controls

| Hotkey | Action | Description |
|--------|--------|-------------|
| **Ctrl + Space** | Start Recording | Begin voice capture |
| **Enter** | Stop & Transcribe | End recording and convert to text |
| **Escape** (optional) | Cancel | Stop recording without typing |

### What Happens During Recording

1. **Microphone Activates** - Audio input stream starts
2. **Visual Feedback** - Floating pill shows animated bars
3. **Voice Level Detection** - Real-time dB meter
4. **Audio Buffering** - Stores audio in memory

### What Happens After Stopping

1. **Transcription** - Converts audio to text
2. **Text Normalization** - Removes noise, filler words, fixes punctuation
3. **Clipboard Copy** - Puts text in clipboard + trailing space
4. **Auto-Paste** - Ctrl+V to type into active app
5. **Clipboard Restore** - Restores your previous clipboard content

---

## ⚙️ Setup & Configuration

### Edit Configuration (Optional)

Open `whisperflow.pyw` and modify these settings:

```python
# Line 17-18: Audio capture settings
SAMPLE_RATE = 16000        # Hz (16kHz standard for Whisper)
BLOCK_SIZE = 512           # Sample frames per buffer (lower = lower latency)

# Line 21: Whisper model selection
model = WhisperModel('tiny.en', device='cpu', compute_type='int8')
#                     ^^^^^^^^
# Options: 'tiny.en', 'base.en', 'small.en', 'medium.en', 
#          'tiny', 'base', 'small', 'medium', 'large'

# Line 31-32: Audio level detection (dB range)
LOWER_DB = -58.0           # Silence threshold
UPPER_DB = 0.0             # Maximum sound level

# Line 103-105: Floating UI size
WIDTH = 142                # Pill width in pixels
HEIGHT = 44                # Pill height in pixels
RADIUS = HEIGHT // 2       # Rounded corner radius

# Line 267-268: Hotkeys
keyboard.add_hotkey('ctrl+space', start_recording)   # Change to preferred hotkey
keyboard.add_hotkey('enter', stop_and_paste)         # Change to preferred hotkey
```

### Advanced Configuration

```python
# Model inference settings (line 207-213)
beam_size=1                # Beam search width (higher = more accurate but slower)
best_of=1                  # Number of candidates (1 for speed)
temperature=0.0            # Randomness (0 = deterministic)
condition_on_previous_text=False  # Use context from previous text

# Smoothing factor for audio visualization (line 187)
smoothing = 0.55 if norm_level > smoothed_audio_level else 0.18
#           ^^^^                                              ^^^^
#           Attack (rising)                          Release (falling)
```

---

## 🪟 Windows Startup Setup

### Option 1: Add to Windows Startup (Runs on Boot)

#### Method A: Using Startup Folder

1. **Open Startup Folder:**
   - Press `Win + R`
   - Type: `shell:startup`
   - Press Enter

2. **Create Shortcut:**
   - Right-click in the folder → **New** → **Shortcut**
   - In location field, paste:
     ```
     C:\path\to\python.exe C:\path\to\typeo\whisperflow.pyw
     ```
   - Replace paths with your actual paths
   - Click **Next** → Name it "WhisperFlow" → **Finish**

3. **Verify:**
   - Restart your computer
   - WhisperFlow should start automatically

#### Method B: Using Registry (Advanced)

1. **Press Win + R**, type `regedit`, press Enter
2. **Navigate to:**
   ```
   HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Run
   ```
3. **Right-click** → **New** → **String Value**
4. **Name it:** `WhisperFlow`
5. **Value:** 
   ```
   "C:\path\to\python.exe" "C:\path\to\typeo\whisperflow.pyw"
   ```

### Option 2: Create Windows Batch File

1. **Create `start_whisperflow.bat`:**
   ```batch
   @echo off
   cd C:\path\to\typeo
   python whisperflow.pyw
   pause
   ```

2. **Move to Startup folder:**
   - Cut the `.bat` file
   - Open: `C:\Users\YOUR_USERNAME\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup`
   - Paste the file

### Option 3: Use Task Scheduler (Best for Auto-Restart)

1. **Open Task Scheduler:**
   - Press `Win + R`
   - Type: `taskschd.msc`
   - Press Enter

2. **Create Basic Task:**
   - Right-click → **Create Basic Task**
   - Name: `WhisperFlow`
   - Description: `Voice-to-text typing assistant`

3. **Set Trigger:**
   - Select: **At log on**
   - Choose: **Specific user** (your account)
   - Click **Next**

4. **Set Action:**
   - Action: **Start a program**
   - Program: `C:\path\to\python.exe`
   - Arguments: `C:\path\to\typeo\whisperflow.pyw`
   - Click **Next** → **Finish**

5. **Test:**
   - Right-click task → **Run**
   - WhisperFlow should start

---

## 🖱️ What Gets Typed (Hotkey Terminology)

### Hotkey Components

| Term | Meaning | Example |
|------|---------|---------|
| **Ctrl** | Control key | Ctrl+Space = Control + Spacebar |
| **Space** | Spacebar | Press the spacebar |
| **Enter** | Return key | Press the Enter/Return key |
| **Shift** | Shift key | Shift+A = Capital A |
| **Alt** | Alternate key | Alt+Tab = Switch windows |
| **Win** | Windows key | Win+D = Show desktop |

### Custom Hotkey Examples

To change hotkeys, edit lines 267-268:

```python
# Example 1: Use Alt+V to start recording
keyboard.add_hotkey('alt+v', start_recording)

# Example 2: Use any key to stop
keyboard.add_hotkey('esc', stop_and_paste)  # Press Escape to stop

# Example 3: Use mouse button (requires pynput)
# from pynput import mouse
# listener.on_click(start_recording)
```

---

## 🐛 Troubleshooting

### **Microphone Not Detected**
```
[ERROR] Audio device not found
```
**Solution:**
- Check if microphone is plugged in
- Go to Settings → Sound → Check "Input volume"
- Try different audio device (edit SAMPLE_RATE settings)
- Restart the application

### **Whisper Model Download Fails**
```
[ERROR] Cannot download model
```
**Solution:**
- Check internet connection
- Manually download: https://github.com/openai/whisper/discussions
- Ensure 1-2 GB free disk space
- Try smaller model: `tiny.en` instead of `base.en`

### **Text Not Typing Into Application**
**Solution:**
- Make sure target application window is **active** (has focus)
- Click into the text field first before pressing hotkey
- Check if application blocks auto-typing (some security software)
- Try running as Administrator:
  - Right-click `whisperflow.pyw` → **Run as administrator**

### **Poor Recognition / Lots of Errors**
**Solution:**
- Speak clearly and slowly
- Use external microphone for better quality
- Reduce background noise
- Use larger model: Change `tiny.en` to `base.en` or `small.en`
- Check microphone input level in Windows Settings

### **Application Crashes on Startup**
**Solution:**
- Ensure Python 3.8+ is installed:
  ```bash
  python --version
  ```
- Reinstall dependencies:
  ```bash
  pip install --upgrade -r requirements.txt
  ```
- Check if another instance is running (close it first)
- Check disk space (need 1+ GB free)

### **Hotkey Not Working**
**Solution:**
- Close the application and run as Administrator
- Try different hotkey combination
- Check if hotkey conflicts with Windows shortcuts
- On Linux/Mac, may need root permissions

### **Floating UI Not Visible**
**Solution:**
- Check if it's behind other windows (press hotkey to bring to front)
- Ensure display scaling is at 100% (Windows Settings → Display)
- Try restarting the application

### **Slow Transcription / Freezes**
**Solution:**
- Use faster model: `tiny.en` (default)
- Close other applications to free RAM
- Check CPU usage in Task Manager
- Reduce audio block size (BLOCK_SIZE = 256)
- Disable other background services

---

## 🔍 How It Works

### 1. **Audio Capture** 🎙️
- Opens audio input stream at 16kHz sample rate
- Captures 512-sample frames in real-time
- Calculates audio level in decibels (dB)

### 2. **Voice Level Detection** 📊
- Converts raw audio to RMS (Root Mean Square)
- Calculates dB level: `20 × log10(RMS)`
- Clamps between -58dB (silence) and 0dB (max)
- Smooths level with exponential moving average

### 3. **Visual Feedback** 🎨
- Displays 4 animated bars
- Bar height corresponds to voice level
- Sine wave animation adds movement
- Updates every 16ms for smooth animation

### 4. **Audio Buffering** 💾
- Stores audio frames in memory during recording
- Concatenates all frames when recording stops
- Converts to WAV format with scipy.io.wavfile

### 5. **Transcription** 🤖
- Sends WAV to Whisper AI model
- Whisper processes audio and returns segments
- Each segment contains recognized text

### 6. **Text Normalization** 🧹
- Removes placeholder patterns: `[BLANK_AUDIO]`, `<|nospeech|>`
- Filters out noise descriptions: `[applause]`, `[background noise]`
- Removes filler words: `um`, `uh`, `hmm`, `erm`
- Fixes punctuation and extra spaces
- Smart trailing period detection

### 7. **Clipboard Management** 📋
1. **Snapshot** - Saves current clipboard content
2. **Copy** - Puts transcribed text + space in clipboard
3. **Paste** - Simulates Ctrl+V to type into application
4. **Restore** - Replaces clipboard with original content

---

## 📝 Text Normalization Examples

| Input | Output |
|-------|--------|
| `Hello, um, world [applause]` | `Hello world` |
| `This is an email test@example.com.` | `test@example.com` (period removed) |
| `The number is (uh) one two three` | `The number is one two three` |
| `Visit www.google.com [background noise]` | `Visit www.google.com` |
| `Hmm, I think (yeah) so` | `I think so` |

---

## 🔐 Privacy & Security

- ✅ **Local Processing**: All audio stays on your computer
- ✅ **No Cloud**: No data sent to external servers
- ✅ **No Recording**: Audio is not stored or logged
- ✅ **Clipboard Safe**: Original clipboard restored after typing
- ✅ **Open Source**: Full code transparency

---

## 📦 Dependencies Explained

```
numpy>=1.24.0              # Array operations for audio signals
scipy>=1.10.0              # WAV file I/O, scientific functions
sounddevice>=0.4.5         # Real-time microphone input
keyboard>=0.13.5           # Global hotkey listening (needs admin)
pyperclip>=1.8.2           # Copy/paste system clipboard
pyautogui>=0.9.54          # Simulate keyboard input (Ctrl+V)
faster-whisper>=0.10.0     # Fast Whisper inference engine
```

---

## 🎯 Use Cases

- 📝 **Writing & Blogging** - Faster content creation
- 💼 **Professional** - Hands-free note-taking in meetings
- ♿ **Accessibility** - Alternative input for mobility-limited users
- 🎮 **Gaming** - Voice commands in games
- 📚 **Education** - Transcribe lectures and notes
- 🏥 **Medical** - Sterile voice-to-text for healthcare

---

## 🚀 Performance Tips

1. **Use Tiny Model** - Fastest, suitable for most users
2. **Close Unnecessary Apps** - Free up RAM for faster processing
3. **External Microphone** - Better quality = better recognition
4. **Quiet Environment** - Reduces noise filtering overhead
5. **Regular Restarts** - Clears memory and maintains performance
6. **SSD Storage** - Faster model loading compared to HDD

---

## 📧 Support & Issues

For problems or suggestions:
- **Email**: prakashabhiman@gmail.com
- **GitHub Issues**: [Report a bug](https://github.com/bhargav-maker/typeo/issues)
- **GitHub Discussions**: [Ask a question](https://github.com/bhargav-maker/typeo/discussions)

---

## 📄 License

This project is licensed under the **MIT License** - see the LICENSE file for details.

---

## 🙏 Acknowledgments

- **OpenAI Whisper** - Speech recognition model
- **faster-whisper** - Fast inference implementation
- **Python Community** - For excellent libraries

---

## ⭐ If You Found This Helpful

Please give this project a star! It helps more people discover this voice-to-text solution.

---

**Made with ❤️ by [bhargav-maker](https://github.com/bhargav-maker)**

**Press `Ctrl + Space` to start typing with your voice! 🎤**
