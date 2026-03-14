"""Tests for tuning presets and frequency maps."""

from app.models import TuningPreset
from app.tuning import (
    ALL_PRESETS,
    DEFAULT_PRESET,
    D_DORIAN_FREQUENCIES,
    D_DORIAN_NOTES,
    PRESET_D_DORIAN,
    PRESET_DARK,
    PRESET_DRONE,
    get_preset_by_name,
)


class TestTuningPreset:
    def test_default_preset_is_d_dorian(self):
        assert DEFAULT_PRESET.name == "Davidic D Dorian"

    def test_d_dorian_has_eight_notes(self):
        assert len(PRESET_D_DORIAN.notes) == 8
        assert len(PRESET_D_DORIAN.frequencies) == 8

    def test_d_dorian_frequencies_ascending(self):
        for i in range(len(D_DORIAN_FREQUENCIES) - 1):
            assert D_DORIAN_FREQUENCIES[i] < D_DORIAN_FREQUENCIES[i + 1]

    def test_d_dorian_starts_with_d2(self):
        assert D_DORIAN_NOTES[0] == "D2"
        assert D_DORIAN_FREQUENCIES[0] == 73.42

    def test_d_dorian_ends_with_d3(self):
        assert D_DORIAN_NOTES[-1] == "D3"
        assert D_DORIAN_FREQUENCIES[-1] == 146.83

    def test_dark_mode_preset_has_bb2(self):
        assert "Bb2" in PRESET_DARK.notes

    def test_drone_preset_higher_range(self):
        assert PRESET_DRONE.frequencies[-1] > PRESET_D_DORIAN.frequencies[-1]

    def test_all_presets_has_three_entries(self):
        assert len(ALL_PRESETS) == 3

    def test_get_preset_by_name_found(self):
        result = get_preset_by_name("Davidic D Dorian")
        assert result is not None
        assert result.name == "Davidic D Dorian"

    def test_get_preset_by_name_not_found(self):
        assert get_preset_by_name("nonexistent") is None

    def test_preset_notes_frequencies_length_match(self):
        for p in ALL_PRESETS:
            assert len(p.notes) == len(p.frequencies)
