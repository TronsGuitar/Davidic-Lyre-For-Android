"""Sample-based audio engine with polyphony support.

The engine generates simple sine-wave tones as placeholders until real
WAV samples are provided.  On Android the Kivy SoundLoader backend
will be used; on desktop we fall back to generated tones when samples
are unavailable.
"""

from __future__ import annotations

import array
import math
import os
import struct
import wave

from app.config import ATTACK, DECAY, SUSTAIN, RELEASE


def _wav_path(note: str) -> str:
    """Return the expected path for a string's WAV sample."""
    return os.path.join("assets", "audio", f"lyre_{note}.wav")


def generate_placeholder_wav(
    path: str,
    frequency: float,
    duration: float = 1.5,
    sample_rate: int = 44100,
    amplitude: float = 0.6,
) -> None:
    """Write a simple sine-wave WAV file as a placeholder sample.

    The tone applies a basic ADSR envelope so it sounds more like a
    plucked string than a raw sine wave.
    """
    n_samples = int(sample_rate * duration)
    samples: list[int] = []
    for i in range(n_samples):
        t = i / sample_rate
        # ADSR envelope
        if t < ATTACK:
            env = t / ATTACK
        elif t < ATTACK + DECAY:
            env = 1.0 - (1.0 - SUSTAIN) * ((t - ATTACK) / DECAY)
        elif t < duration - RELEASE:
            env = SUSTAIN
        else:
            env = SUSTAIN * ((duration - t) / RELEASE)
        env = max(0.0, env)
        value = amplitude * env * math.sin(2.0 * math.pi * frequency * t)
        samples.append(int(value * 32767))

    os.makedirs(os.path.dirname(path), exist_ok=True)
    raw = array.array("h", samples)
    with wave.open(path, "w") as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(sample_rate)
        wf.writeframes(raw.tobytes())


def ensure_samples(notes: list[str], frequencies: list[float]) -> dict[str, str]:
    """Ensure WAV files exist for every note, generating placeholders as needed.

    Returns a mapping of note name → file path.
    """
    paths: dict[str, str] = {}
    for note, freq in zip(notes, frequencies):
        p = _wav_path(note)
        if not os.path.exists(p):
            generate_placeholder_wav(p, freq)
        paths[note] = p
    return paths


class AudioEngine:
    """Lightweight audio engine wrapping Kivy's ``SoundLoader``.

    Falls back gracefully when Kivy is not available (e.g. during testing).
    """

    def __init__(self) -> None:
        self._sounds: dict[str, object] = {}
        self._loader = None
        try:
            from kivy.core.audio import SoundLoader  # type: ignore[import]
            self._loader = SoundLoader
        except Exception:
            pass

    def load(self, note: str, path: str) -> None:
        """Pre-load a sample for *note* from *path*."""
        if self._loader is None:
            return
        sound = self._loader.load(path)
        if sound is not None:
            self._sounds[note] = sound

    def play(self, note: str, velocity: float = 1.0) -> None:
        """Play the sample for *note* at the given *velocity* (gain)."""
        sound = self._sounds.get(note)
        if sound is None:
            return
        sound.volume = max(0.0, min(1.0, velocity))  # type: ignore[union-attr]
        sound.play()  # type: ignore[union-attr]

    def stop(self, note: str) -> None:
        """Stop (mute) the sample for *note*."""
        sound = self._sounds.get(note)
        if sound is not None:
            sound.stop()  # type: ignore[union-attr]

    def stop_all(self) -> None:
        """Stop all currently playing sounds."""
        for sound in self._sounds.values():
            sound.stop()  # type: ignore[union-attr]
