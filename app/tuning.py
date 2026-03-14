"""
app/tuning.py – Note names, frequency maps, and tuning preset definitions.

All frequency values are in Hz; note names use standard scientific pitch
notation (e.g. "D2", "A2").
"""

from dataclasses import dataclass, field
from typing import List


# ---------------------------------------------------------------------------
# Standard equal-temperament frequencies (Hz) for reference notes
# ---------------------------------------------------------------------------
NOTE_FREQ: dict[str, float] = {
    "D2":  73.42,
    "E2":  82.41,
    "F2":  87.31,
    "G2":  98.00,
    "A2": 110.00,
    "Bb2": 116.54,
    "B2": 123.47,
    "C3": 130.81,
    "D3": 146.83,
    "F3": 174.61,
    "G3": 196.00,
    "A3": 220.00,
    "C4": 261.63,
    "D4": 293.66,
}


# ---------------------------------------------------------------------------
# TuningPreset dataclass
# ---------------------------------------------------------------------------
@dataclass
class TuningPreset:
    """Describes a named tuning configuration for the 8-string lyre."""
    name: str
    notes: List[str]
    frequencies: List[float]

    def __post_init__(self) -> None:
        if len(self.notes) != 8:
            raise ValueError(
                f"TuningPreset '{self.name}' must have exactly 8 notes, "
                f"got {len(self.notes)}."
            )
        if len(self.frequencies) != 8:
            raise ValueError(
                f"TuningPreset '{self.name}' must have exactly 8 frequencies, "
                f"got {len(self.frequencies)}."
            )
        for i, f in enumerate(self.frequencies):
            if f <= 0:
                raise ValueError(
                    f"Frequency at index {i} must be positive, got {f}."
                )

    def sample_filename(self, index: int) -> str:
        """Return the WAV filename for string *index* (0-based)."""
        note = self.notes[index].replace("#", "s")
        return f"lyre_{note}.wav"

    def sample_filenames(self) -> List[str]:
        """Return all WAV filenames for this preset."""
        return [self.sample_filename(i) for i in range(8)]


# ---------------------------------------------------------------------------
# Built-in presets
# ---------------------------------------------------------------------------
def _build_preset(name: str, notes: List[str]) -> TuningPreset:
    freqs = [NOTE_FREQ[n] for n in notes]
    return TuningPreset(name=name, notes=notes, frequencies=freqs)


PRESET_D_DORIAN = _build_preset(
    "Davidic D Dorian",
    ["D2", "E2", "F2", "G2", "A2", "B2", "C3", "D3"],
)

PRESET_DARK = _build_preset(
    "Davidic Dark Mode",
    ["D2", "E2", "F2", "G2", "A2", "Bb2", "C3", "D3"],
)

PRESET_DRONE = _build_preset(
    "Drone Psalm",
    ["D2", "A2", "D3", "F3", "G3", "A3", "C4", "D4"],
)

ALL_PRESETS: List[TuningPreset] = [PRESET_D_DORIAN, PRESET_DARK, PRESET_DRONE]
DEFAULT_PRESET = PRESET_D_DORIAN


def get_preset_by_name(name: str) -> TuningPreset:
    """Return a preset by exact name, or the default if not found."""
    for p in ALL_PRESETS:
        if p.name == name:
            return p
    return DEFAULT_PRESET
"""Note names, frequency maps, and tuning preset definitions."""

from app.models import TuningPreset


# Default tuning: D Dorian
D_DORIAN_NOTES = ["D2", "E2", "F2", "G2", "A2", "B2", "C3", "D3"]
D_DORIAN_FREQUENCIES = [73.42, 82.41, 87.31, 98.00, 110.00, 123.47, 130.81, 146.83]

# Alternate dark preset
DARK_MODE_NOTES = ["D2", "E2", "F2", "G2", "A2", "Bb2", "C3", "D3"]
DARK_MODE_FREQUENCIES = [73.42, 82.41, 87.31, 98.00, 110.00, 116.54, 130.81, 146.83]

# Drone psalm preset
DRONE_PSALM_NOTES = ["D2", "A2", "D3", "F3", "G3", "A3", "C4", "D4"]
DRONE_PSALM_FREQUENCIES = [73.42, 110.00, 146.83, 174.61, 196.00, 220.00, 261.63, 293.66]

# Preset definitions
PRESET_D_DORIAN = TuningPreset(
    name="Davidic D Dorian",
    notes=D_DORIAN_NOTES,
    frequencies=D_DORIAN_FREQUENCIES,
)

PRESET_DARK = TuningPreset(
    name="Davidic Dark Mode",
    notes=DARK_MODE_NOTES,
    frequencies=DARK_MODE_FREQUENCIES,
)

PRESET_DRONE = TuningPreset(
    name="Drone Psalm",
    notes=DRONE_PSALM_NOTES,
    frequencies=DRONE_PSALM_FREQUENCIES,
)

ALL_PRESETS = [PRESET_D_DORIAN, PRESET_DARK, PRESET_DRONE]
DEFAULT_PRESET = PRESET_D_DORIAN


def get_preset_by_name(name: str) -> TuningPreset | None:
    """Return the preset matching *name*, or ``None``."""
    for p in ALL_PRESETS:
        if p.name == name:
            return p
    return None
