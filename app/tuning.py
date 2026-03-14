"""
app/tuning.py — Note names, frequency maps, and preset definitions.

Provides the three built-in tuning presets described in PRD Section 7, plus
helper utilities for resolving note names to frequencies.  Future phases will
extend this module to support manual retuning (PRD Section 18).
"""

from typing import Dict, List

# ---------------------------------------------------------------------------
# Frequency map — standard equal-temperament reference values (Hz)
# ---------------------------------------------------------------------------

NOTE_FREQUENCIES: Dict[str, float] = {
    "D2": 73.42,
    "E2": 82.41,
    "F2": 87.31,
    "G2": 98.00,
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
# Tuning presets (PRD Section 7)
# ---------------------------------------------------------------------------

# Default preset — Davidic D Dorian
PRESET_DAVIDIC_D_DORIAN: Dict = {
    "name": "Davidic D Dorian",
    "notes": ["D2", "E2", "F2", "G2", "A2", "B2", "C3", "D3"],
    "frequencies": [73.42, 82.41, 87.31, 98.00, 110.00, 123.47, 130.81, 146.83],
}

# Alternate dark preset — flattened seventh
PRESET_DAVIDIC_DARK_MODE: Dict = {
    "name": "Davidic Dark Mode",
    "notes": ["D2", "E2", "F2", "G2", "A2", "Bb2", "C3", "D3"],
    "frequencies": [73.42, 82.41, 87.31, 98.00, 110.00, 116.54, 130.81, 146.83],
}

# Drone/open-string preset for psalm accompaniment
PRESET_DRONE_PSALM: Dict = {
    "name": "Drone Psalm",
    "notes": ["D2", "A2", "D3", "F3", "G3", "A3", "C4", "D4"],
    "frequencies": [73.42, 110.00, 146.83, 174.61, 196.00, 220.00, 261.63, 293.66],
}

# Ordered list used for the UI preset dropdown
ALL_PRESETS: List[Dict] = [
    PRESET_DAVIDIC_D_DORIAN,
    PRESET_DAVIDIC_DARK_MODE,
    PRESET_DRONE_PSALM,
]

DEFAULT_PRESET: Dict = PRESET_DAVIDIC_D_DORIAN

# ---------------------------------------------------------------------------
# Helper utilities
# ---------------------------------------------------------------------------


def get_frequency(note_name: str) -> float:
    """Return the frequency (Hz) for a given note name.

    Args:
        note_name: Note identifier string, e.g. ``"D2"``, ``"Bb2"``.

    Returns:
        Frequency in Hz.

    Raises:
        KeyError: If *note_name* is not present in the frequency map.
    """
    return NOTE_FREQUENCIES[note_name]


def get_preset_by_name(name: str) -> Dict:
    """Return the preset dict whose ``name`` key matches *name*.

    Args:
        name: Human-readable preset name, e.g. ``"Davidic D Dorian"``.

    Returns:
        Preset dictionary with ``name``, ``notes``, and ``frequencies`` keys.

    Raises:
        ValueError: If no preset with the given name exists.
    """
    for preset in ALL_PRESETS:
        if preset["name"] == name:
            return preset
    raise ValueError(f"Unknown tuning preset: {name!r}")


# TODO: Implement manual retuning helpers (Phase V2 — PRD Section 18)
# def retune_string(preset, string_index, new_note_name): ...
