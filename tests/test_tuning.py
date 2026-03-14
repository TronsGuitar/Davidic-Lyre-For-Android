"""
tests/test_tuning.py – Unit tests for app.tuning module.

These tests run without Kivy; they exercise only pure-Python logic.
"""

import pytest

from app.tuning import (
    ALL_PRESETS,
    DEFAULT_PRESET,
    NOTE_FREQ,
    PRESET_D_DORIAN,
    PRESET_DARK,
    PRESET_DRONE,
    TuningPreset,
    get_preset_by_name,
)


class TestNoteFrequencies:
    def test_d2_frequency(self):
        assert abs(NOTE_FREQ["D2"] - 73.42) < 0.01

    def test_a2_frequency(self):
        assert abs(NOTE_FREQ["A2"] - 110.00) < 0.01

    def test_all_frequencies_positive(self):
        for name, freq in NOTE_FREQ.items():
            assert freq > 0, f"Frequency for {name} must be positive"


class TestTuningPreset:
    def test_d_dorian_has_eight_strings(self):
        assert len(PRESET_D_DORIAN.notes) == 8
        assert len(PRESET_D_DORIAN.frequencies) == 8

    def test_d_dorian_starts_on_d2(self):
        assert PRESET_D_DORIAN.notes[0] == "D2"
        assert abs(PRESET_D_DORIAN.frequencies[0] - 73.42) < 0.01

    def test_d_dorian_ends_on_d3(self):
        assert PRESET_D_DORIAN.notes[-1] == "D3"
        assert abs(PRESET_D_DORIAN.frequencies[-1] - 146.83) < 0.01

    def test_dark_preset_has_bb2(self):
        assert "Bb2" in PRESET_DARK.notes

    def test_drone_preset_has_f3(self):
        assert "F3" in PRESET_DRONE.notes

    def test_preset_frequencies_ascending(self):
        """D Dorian strings should ascend in pitch."""
        freqs = PRESET_D_DORIAN.frequencies
        for i in range(len(freqs) - 1):
            assert freqs[i] < freqs[i + 1], (
                f"String {i} ({freqs[i]} Hz) should be lower than "
                f"string {i+1} ({freqs[i+1]} Hz)"
            )

    def test_sample_filename_no_sharps(self):
        preset = PRESET_D_DORIAN
        for i in range(8):
            fname = preset.sample_filename(i)
            assert "#" not in fname, f"Filename {fname} must not contain '#'"
            assert fname.endswith(".wav")

    def test_sample_filenames_count(self):
        assert len(PRESET_D_DORIAN.sample_filenames()) == 8

    def test_invalid_preset_too_few_notes(self):
        with pytest.raises(ValueError):
            TuningPreset(name="bad", notes=["D2"], frequencies=[73.42])

    def test_invalid_preset_negative_frequency(self):
        with pytest.raises(ValueError):
            TuningPreset(
                name="bad",
                notes=["D2", "E2", "F2", "G2", "A2", "B2", "C3", "D3"],
                frequencies=[-1, 82, 87, 98, 110, 123, 131, 147],
            )


class TestAllPresets:
    def test_three_presets_defined(self):
        assert len(ALL_PRESETS) == 3

    def test_default_is_d_dorian(self):
        assert DEFAULT_PRESET.name == "Davidic D Dorian"

    def test_get_preset_by_name_returns_correct(self):
        preset = get_preset_by_name("Davidic Dark Mode")
        assert preset.name == "Davidic Dark Mode"

    def test_get_preset_unknown_name_returns_default(self):
        preset = get_preset_by_name("NonExistent")
        assert preset is DEFAULT_PRESET

    def test_all_presets_valid(self):
        for p in ALL_PRESETS:
            assert len(p.notes) == 8
            assert len(p.frequencies) == 8
            for f in p.frequencies:
                assert f > 0
