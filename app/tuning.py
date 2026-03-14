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
