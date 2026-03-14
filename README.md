# Davidic Lyre for Android

A touch-based digital lyre inspired by the ancient Hebrew *kinnor*.  Tap to
pluck, swipe to strum, hold to mute — built with Python and Kivy for Android
(Samsung Galaxy Fold5).

## Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Run on desktop
python main.py
```

## Project Structure

```
main.py                 # Kivy app entry point
app/
├── config.py           # Constants, thresholds, colour palette
├── tuning.py           # Note names, frequencies, presets
├── models.py           # LyreString, TouchTrace, TuningPreset
├── gestures.py         # Tap / swipe / hold detection
├── audio_engine.py     # Sample loading and playback
├── lyre_widget.py      # Kivy widget: drawing + touch routing
├── controls.py         # Header bar, tuning dropdown
└── screens.py          # Main instrument screen
assets/
├── audio/              # WAV samples (auto-generated placeholders)
└── images/             # Textures (future)
tests/                  # pytest test suite
```

## Running Tests

```bash
pip install pytest
python -m pytest tests/ -v
```

## Building for Android

```bash
pip install buildozer
buildozer android debug
```

See `buildozer.spec` for packaging configuration.

## Default Tuning

**Davidic D Dorian** — D2 · E2 · F2 · G2 · A2 · B2 · C3 · D3
