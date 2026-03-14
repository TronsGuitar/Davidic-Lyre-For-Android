# Davidic Lyre for Android

> A Python/Kivy mobile instrument that brings an ancient 8-string lyre to your fingertips.

---

## Overview

**Davidic Lyre for Android** is a Python/Kivy mobile app simulating an ancient David-style 8-string lyre for Android (Samsung Galaxy Fold5). It delivers a warm, gut-string tone through touch-based interactions — tap to pluck, swipe to strum, hold to mute — and ships with historically inspired tuning presets drawn from ancient Near Eastern scales.

---

## Features

- 🎵 **8-string lyre simulation** — full instrument layout optimised for the Galaxy Fold5 inner screen
- 👆 **Tap-to-pluck** — touch any string to produce an immediate pluck sound
- 🤚 **Swipe strumming** — drag across strings to strum in playing order with natural sequential timing
- ✋ **Hold-to-mute** — hold a finger on a ringing string to damp it; drag to mute multiple strings
- 🎼 **Historically inspired tuning presets** — D Dorian, Dark Mode (Phrygian flavour), and Drone Psalm open tuning
- 🌊 **String vibration animation** — visual oscillation on pluck, decaying with the audio envelope
- 🔊 **Drone mode** — sustain the lowest string for psalm-style accompaniment
- 📱 **Fold5-optimised layout** — portrait unfolded mode is the primary target; gracefully scales to the outer screen

---

## Tech Stack

| Layer | Technology |
|---|---|
| Language | Python 3.11 |
| UI & Input | [Kivy](https://kivy.org/) |
| Android Packaging | [Buildozer](https://buildozer.readthedocs.io/) |
| Android Bridge | pyjnius |
| Device APIs | plyer |
| Target Platform | Android API 34 (min API 26) |

---

## Build Instructions

### Prerequisites

- Python 3.11
- Linux or macOS build host (required by Buildozer)
- Android SDK / NDK (installed automatically by Buildozer on first run)

### Steps

```bash
# 1. Clone the repository
git clone https://github.com/TronsGuitar/Davidic-Lyre-For-Android.git
cd Davidic-Lyre-For-Android

# 2. Install Python dependencies
pip install -r requirements.txt

# 3. Run locally on your desktop (for UI development)
python main.py

# 4. Build the Android debug APK
buildozer android debug

# 5. Deploy and run on a connected Android device
buildozer android deploy run
```

> **Note:** Place WAV sample files in `assets/audio/` and image assets in `assets/images/` before building. See the README files in each directory for details.

---

## Project Structure

```
.
├── PRD.md                    # Product Requirements Document
├── README.md                 # This file
├── requirements.txt          # Python dependencies
├── buildozer.spec            # Android build configuration
├── main.py                   # App entry point (DavidicLyreApp)
├── assets/
│   ├── audio/                # WAV samples — one per string (lyre_D2.wav … lyre_D3.wav)
│   │   └── README.md
│   └── images/               # Icon, presplash, and texture images
│       └── README.md
├── app/
│   ├── __init__.py           # Package init
│   ├── config.py             # Constants, thresholds, color palette
│   ├── tuning.py             # Note names, frequency maps, preset definitions
│   ├── models.py             # LyreString, TouchTrace, TuningPreset dataclasses
│   ├── gestures.py           # Tap, swipe, and hold gesture recognition
│   ├── audio_engine.py       # Sample loading, ADSR envelopes, polyphony
│   ├── lyre_widget.py        # Kivy canvas rendering and touch routing
│   ├── controls.py           # UI controls — preset picker, toggles, sliders
│   └── screens.py            # Screen hierarchy — MainScreen, SettingsPopup
└── tests/
    ├── test_tuning.py        # Tuning preset and frequency map tests
    ├── test_gestures.py      # Gesture detection algorithm tests
    └── test_string_model.py  # LyreString and data model tests
```

---

## Tuning Presets

| Preset | Strings (low → high) | Character |
|---|---|---|
| **Davidic D Dorian** *(default)* | D2 · E2 · F2 · G2 · A2 · B2 · C3 · D3 | Bright modal sound of ancient Hebrew kinnor |
| **Davidic Dark Mode** | D2 · E2 · F2 · G2 · A2 · B♭2 · C3 · D3 | Darker Phrygian-adjacent flavour |
| **Drone Psalm** | D2 · A2 · D3 · F3 · G3 · A3 · C4 · D4 | Open drone tuning for psalm accompaniment |

---

## License

*License placeholder — to be determined.*
