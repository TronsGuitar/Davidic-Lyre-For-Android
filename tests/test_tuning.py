"""
tests/test_tuning.py — Tests for tuning presets and frequency maps.

Validates that:
  - All three tuning presets are defined with the correct note names and
    frequencies as specified in PRD Section 7.
  - The NOTE_FREQUENCIES map contains expected values.
  - Helper utilities (get_frequency, get_preset_by_name) behave correctly.

TODO: Expand with property-based tests and edge-case coverage in Phase 1.
"""

import pytest

from app.tuning import (
    ALL_PRESETS,
    DEFAULT_PRESET,
    NOTE_FREQUENCIES,
    PRESET_DAVIDIC_D_DORIAN,
    PRESET_DAVIDIC_DARK_MODE,
    PRESET_DRONE_PSALM,
    get_frequency,
    get_preset_by_name,
)


# ---------------------------------------------------------------------------
# Placeholder — always passes; replace with real assertions in Phase 1
# ---------------------------------------------------------------------------


def test_placeholder():
    """Placeholder test — confirms the module imports without error."""
    # TODO: Replace with comprehensive tuning tests in Phase 1
    assert True


# ---------------------------------------------------------------------------
# Preset structure tests
# ---------------------------------------------------------------------------


def test_all_presets_have_eight_strings():
    """Each preset must define exactly 8 notes and 8 frequencies."""
    for preset in ALL_PRESETS:
        assert len(preset["notes"]) == 8, (
            f"Preset '{preset['name']}' has {len(preset['notes'])} notes, expected 8"
        )
        assert len(preset["frequencies"]) == 8, (
            f"Preset '{preset['name']}' has {len(preset['frequencies'])} frequencies, expected 8"
        )


def test_default_preset_is_d_dorian():
    """The default preset must be 'Davidic D Dorian'."""
    assert DEFAULT_PRESET["name"] == "Davidic D Dorian"


def test_d_dorian_notes():
    """Davidic D Dorian preset should have the expected note names (PRD Section 7)."""
    expected = ["D2", "E2", "F2", "G2", "A2", "B2", "C3", "D3"]
    assert PRESET_DAVIDIC_D_DORIAN["notes"] == expected


def test_d_dorian_frequencies():
    """Davidic D Dorian preset should have the correct frequencies (PRD Section 7)."""
    expected = [73.42, 82.41, 87.31, 98.00, 110.00, 123.47, 130.81, 146.83]
    assert PRESET_DAVIDIC_D_DORIAN["frequencies"] == pytest.approx(expected, abs=0.01)


def test_dark_mode_has_flattened_seventh():
    """Davidic Dark Mode replaces B2 with Bb2 relative to D Dorian."""
    dorian_notes = PRESET_DAVIDIC_D_DORIAN["notes"]
    dark_notes = PRESET_DAVIDIC_DARK_MODE["notes"]
    # All notes the same except index 5 (the seventh)
    assert dark_notes[5] == "Bb2"
    assert dorian_notes[5] == "B2"


def test_drone_psalm_notes():
    """Drone Psalm preset should have the expected note names (PRD Section 7)."""
    expected = ["D2", "A2", "D3", "F3", "G3", "A3", "C4", "D4"]
    assert PRESET_DRONE_PSALM["notes"] == expected


# ---------------------------------------------------------------------------
# Frequency map tests
# ---------------------------------------------------------------------------


def test_note_frequencies_contains_d2():
    """NOTE_FREQUENCIES must map 'D2' to approximately 73.42 Hz."""
    assert NOTE_FREQUENCIES["D2"] == pytest.approx(73.42, abs=0.01)


def test_get_frequency_known_note():
    """get_frequency should return the correct Hz for a known note."""
    assert get_frequency("A2") == pytest.approx(110.00, abs=0.01)


def test_get_frequency_unknown_note_raises():
    """get_frequency should raise KeyError for an unknown note name."""
    with pytest.raises(KeyError):
        get_frequency("Z99")


# ---------------------------------------------------------------------------
# Preset lookup tests
# ---------------------------------------------------------------------------


def test_get_preset_by_name_returns_correct_preset():
    """get_preset_by_name should return the preset matching the given name."""
    preset = get_preset_by_name("Drone Psalm")
    assert preset["name"] == "Drone Psalm"


def test_get_preset_by_name_unknown_raises():
    """get_preset_by_name should raise ValueError for an unknown name."""
    with pytest.raises(ValueError):
        get_preset_by_name("Nonexistent Preset")
