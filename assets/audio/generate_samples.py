#!/usr/bin/env python3
"""
assets/audio/generate_samples.py
Standalone script to pre-generate all gut-string WAV samples.

Usage:
    python assets/audio/generate_samples.py

The generated files are placed in the same directory as this script.
They can then be committed to the repo so that the app does not need to
generate them at first launch on a low-powered device.
"""

import os
import sys

# Allow running from the repo root or from this directory
_HERE = os.path.dirname(os.path.abspath(__file__))
_ROOT = os.path.join(_HERE, "..", "..")
if _ROOT not in sys.path:
    sys.path.insert(0, _ROOT)

from app.audio_engine import generate_wav_sample  # noqa: E402
from app.tuning import ALL_PRESETS  # noqa: E402


def main() -> None:
    out_dir = _HERE
    seen: set[str] = set()

    for preset in ALL_PRESETS:
        print(f"Preset: {preset.name}")
        for note, freq in zip(preset.notes, preset.frequencies):
            filename = f"lyre_{note.replace('#', 's')}.wav"
            if filename in seen:
                print(f"  {filename:25s}  (already generated)")
                continue
            seen.add(filename)
            filepath = os.path.join(out_dir, filename)
            if os.path.isfile(filepath):
                print(f"  {filename:25s}  (exists, skipping)")
                continue
            print(f"  {filename:25s}  {freq:.2f} Hz … ", end="", flush=True)
            generate_wav_sample(freq, filepath)
            size_kb = os.path.getsize(filepath) // 1024
            print(f"done ({size_kb} kB)")

    print("\nAll samples ready.")


if __name__ == "__main__":
    main()
