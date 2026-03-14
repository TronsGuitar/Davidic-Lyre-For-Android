"""
app/audio_engine.py – Sample-based audio playback engine.

For MVP the engine loads WAV files (or generates them if missing) and
plays them back using Kivy's SoundLoader.  Up to POLYPHONY simultaneous
voices are supported via a pool of Sound objects per string.

If Kivy is not available (e.g. during unit tests) the engine degrades
gracefully: all methods are no-ops but the API surface is identical.
"""

import math
import os
import struct
import wave
from typing import Dict, List, Optional

from app.config import (
    ADSR,
    POLYPHONY,
    SAMPLE_DURATION_S,
    SAMPLE_RATE,
    SYMPATHETIC_MAX,
)
from app.tuning import TuningPreset

# ---------------------------------------------------------------------------
# Attempt to import Kivy audio; fall back to a no-op stub if unavailable.
# ---------------------------------------------------------------------------
try:
    from kivy.core.audio import SoundLoader  # type: ignore
    _KIVY_AUDIO = True
except Exception:  # pragma: no cover – runs without Kivy in tests
    _KIVY_AUDIO = False
    SoundLoader = None  # type: ignore


# ---------------------------------------------------------------------------
# WAV sample generation (pure stdlib – no external dependencies)
# ---------------------------------------------------------------------------

def _apply_adsr(t: float, duration: float) -> float:
    """Return the ADSR envelope value for time *t* within a note of *duration* s."""
    attack  = ADSR["attack"]
    decay   = ADSR["decay"]
    sustain = ADSR["sustain"]
    release = ADSR["release"]

    if t < attack:
        return t / attack
    t -= attack
    if t < decay:
        return 1.0 - (1.0 - sustain) * (t / decay)
    t -= decay
    body = duration - attack - decay - release
    if body > 0 and t < body:
        return sustain
    t -= max(body, 0.0)
    if t < release:
        return sustain * (1.0 - t / release)
    return 0.0


def generate_wav_sample(freq: float, filepath: str) -> None:
    """
    Generate a gut-string-like WAV file at *freq* Hz and save to *filepath*.

    The tone uses the fundamental plus decaying upper harmonics to mimic
    the warm, short-sustain character of a gut string on a wooden body.
    """
    duration   = SAMPLE_DURATION_S
    n_samples  = int(duration * SAMPLE_RATE)
    two_pi     = 2.0 * math.pi
    max_amp    = 32767

    frames: List[bytes] = []

    for i in range(n_samples):
        t   = i / SAMPLE_RATE
        env = _apply_adsr(t, duration)

        # Fundamental + harmonics with progressively faster decay
        sample = (
            0.60 * math.sin(two_pi * freq       * t)
            + 0.22 * math.sin(two_pi * freq * 2 * t) * math.exp(-t * 4.0)
            + 0.10 * math.sin(two_pi * freq * 3 * t) * math.exp(-t * 7.0)
            + 0.05 * math.sin(two_pi * freq * 4 * t) * math.exp(-t * 12.0)
            + 0.03 * math.sin(two_pi * freq * 5 * t) * math.exp(-t * 18.0)
        )

        # Slight pitch drift to simulate wooden body / gut string warmth
        sample += 0.015 * math.sin(two_pi * (freq * 1.0008) * t)

        val = int(sample * env * 0.75 * max_amp)
        val = max(-max_amp - 1, min(max_amp, val))
        frames.append(struct.pack("<h", val))

    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with wave.open(filepath, "wb") as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(SAMPLE_RATE)
        wf.writeframes(b"".join(frames))


# ---------------------------------------------------------------------------
# Voice pool helper
# ---------------------------------------------------------------------------

class _VoicePool:
    """
    Holds up to *size* Kivy Sound objects for one sample file.
    Round-robins through voices to allow polyphony.
    """

    def __init__(self, sample_path: str, size: int = 4) -> None:
        self.sample_path = sample_path
        self._voices: List = []
        self._index: int = 0
        if _KIVY_AUDIO and SoundLoader is not None:
            for _ in range(size):
                snd = SoundLoader.load(sample_path)
                if snd:
                    snd.volume = 1.0
                    self._voices.append(snd)

    def play(self, gain: float = 1.0) -> None:
        if not self._voices:
            return
        snd = self._voices[self._index % len(self._voices)]
        self._index += 1
        snd.volume = max(0.0, min(1.0, gain))
        if snd.state == "play":
            snd.stop()
        snd.play()

    def stop(self) -> None:
        for snd in self._voices:
            try:
                snd.stop()
            except Exception:
                pass


# ---------------------------------------------------------------------------
# AudioEngine
# ---------------------------------------------------------------------------

class AudioEngine:
    """
    Manages sample loading, polyphonic playback, muting, and (optional)
    sympathetic resonance for the 8-string lyre.
    """

    VOICES_PER_STRING = max(2, POLYPHONY // 8)

    def __init__(self) -> None:
        self._pools: Dict[int, _VoicePool] = {}   # string_id → voice pool
        self._gains: Dict[int, float] = {}         # string_id → current gain
        self._preset: Optional[TuningPreset] = None
        self.reverb_amount: float = 0.0            # 0–1 (reserved for future)

    # ------------------------------------------------------------------
    # Initialisation
    # ------------------------------------------------------------------

    def load_preset(
        self,
        preset: TuningPreset,
        audio_dir: str,
    ) -> None:
        """
        Load (or generate) WAV samples for *preset* and prepare voice pools.

        Parameters
        ----------
        preset:    The TuningPreset whose samples to load.
        audio_dir: Directory where WAV files live (or are created).
        """
        self._preset = preset
        self._pools.clear()
        self._gains.clear()

        for i, (note, freq) in enumerate(
            zip(preset.notes, preset.frequencies)
        ):
            filename = f"lyre_{note.replace('#', 's')}.wav"
            filepath = os.path.join(audio_dir, filename)

            if not os.path.isfile(filepath):
                generate_wav_sample(freq, filepath)

            self._pools[i] = _VoicePool(filepath, self.VOICES_PER_STRING)
            self._gains[i] = 1.0

    # ------------------------------------------------------------------
    # Playback control
    # ------------------------------------------------------------------

    def pluck(self, string_id: int, velocity: float = 1.0) -> None:
        """
        Trigger a pluck on *string_id* with the given *velocity* (0–1).

        Velocity scales the playback gain.  Sympathetic resonance is
        applied to harmonically related strings at low amplitude.
        """
        pool = self._pools.get(string_id)
        if pool is None:
            return

        gain = self._gains.get(string_id, 1.0) * max(0.0, min(1.0, velocity))
        pool.play(gain)

        # Optional sympathetic resonance on related strings
        self._apply_sympathetic(string_id, gain)

    def mute(self, string_id: int) -> None:
        """Immediately stop sound on *string_id*."""
        pool = self._pools.get(string_id)
        if pool is not None:
            pool.stop()

    def mute_all(self) -> None:
        """Silence all strings."""
        for pool in self._pools.values():
            pool.stop()

    def set_gain(self, string_id: int, gain: float) -> None:
        """Set per-string gain multiplier (0–1)."""
        self._gains[string_id] = max(0.0, min(1.0, gain))

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    def _apply_sympathetic(self, source_id: int, source_gain: float) -> None:
        """Trigger low-amplitude resonance on harmonically related strings."""
        if self._preset is None:
            return
        src_freq = self._preset.frequencies[source_id]
        amp = source_gain * SYMPATHETIC_MAX

        for i, freq in enumerate(self._preset.frequencies):
            if i == source_id:
                continue
            ratio = freq / src_freq if src_freq > 0 else 0
            # Check for simple harmonic ratio (within 2 % tolerance)
            for n in (2, 3, 0.5, 1.5):
                if abs(ratio - n) < 0.02:
                    pool = self._pools.get(i)
                    if pool:
                        pool.play(amp)
                    break
