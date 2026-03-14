"""Tests for LyreString, TouchTrace, and TuningPreset data models."""

import pytest

from app.models import LyreString, TouchTrace, TuningPreset


class TestTuningPresetModel:
    def test_create_preset(self):
        p = TuningPreset(name="Test", notes=["A", "B"], frequencies=[110, 220])
        assert p.name == "Test"
        assert len(p.notes) == 2

    def test_mismatched_lengths_raises(self):
        with pytest.raises(ValueError):
            TuningPreset(name="Bad", notes=["A"], frequencies=[110, 220])


class TestLyreString:
    def test_default_values(self):
        s = LyreString(idx=0, note="D2", frequency=73.42, thickness=4.5)
        assert s.muted is False
        assert s.ringing is False
        assert s.gain == 1.0
        assert s.vibration == 0.0

    def test_note_name_property(self):
        s = LyreString(idx=0, note="D2", frequency=73.42, thickness=4.5)
        assert s.note_name == "D2"

    def test_mutability(self):
        s = LyreString(idx=0, note="D2", frequency=73.42, thickness=4.5)
        s.muted = True
        s.vibration = 10.0
        assert s.muted is True
        assert s.vibration == 10.0


class TestTouchTrace:
    def test_defaults(self):
        t = TouchTrace(touch_id=1)
        assert t.start_pos == (0.0, 0.0)
        assert t.crossed_strings == []
        assert t.hold_active is False

    def test_crossed_strings_independent(self):
        t1 = TouchTrace(touch_id=1)
        t2 = TouchTrace(touch_id=2)
        t1.crossed_strings.append(0)
        assert len(t2.crossed_strings) == 0
