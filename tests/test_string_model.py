"""
tests/test_string_model.py — Tests for LyreString, TouchTrace, and TuningPreset
data model classes defined in :mod:`app.models`.

Validates that:
  - Dataclass defaults are sensible.
  - Fields can be set and retrieved correctly.
  - LyreString, TouchTrace, and TuningPreset align with PRD Section 15 field
    specifications.

TODO: Add validation logic tests once models enforce field constraints in Phase 1.
"""

import pytest

from app.models import LyreString, TouchTrace, TuningPreset


# ---------------------------------------------------------------------------
# Placeholder — always passes; replace with real assertions in Phase 1
# ---------------------------------------------------------------------------


def test_placeholder():
    """Placeholder test — confirms the module imports without error."""
    # TODO: Replace with comprehensive model tests in Phase 1
    assert True


# ---------------------------------------------------------------------------
# LyreString tests
# ---------------------------------------------------------------------------


def test_lyre_string_default_construction():
    """LyreString should be constructable with no arguments using safe defaults."""
    s = LyreString()
    assert s.id == 0
    assert s.note_name == ""
    assert s.frequency == 0.0
    assert s.muted is False
    assert s.ringing is False
    assert s.gain == 1.0


def test_lyre_string_field_assignment():
    """LyreString fields should accept and return correct values."""
    s = LyreString(
        id=3,
        note_name="G2",
        frequency=98.00,
        x=150.0,
        y_top=80.0,
        y_bottom=600.0,
        thickness_px=3.5,
        hitbox_width_px=44.0,
        muted=False,
        ringing=True,
        gain=0.9,
        sample_path="assets/audio/lyre_G2.wav",
    )
    assert s.id == 3
    assert s.note_name == "G2"
    assert s.frequency == pytest.approx(98.00)
    assert s.ringing is True
    assert s.sample_path == "assets/audio/lyre_G2.wav"


def test_lyre_string_mute_toggle():
    """Muted flag should be mutable after construction."""
    s = LyreString(id=0, note_name="D2", frequency=73.42)
    assert s.muted is False
    s.muted = True
    assert s.muted is True


# ---------------------------------------------------------------------------
# TouchTrace tests
# ---------------------------------------------------------------------------


def test_touch_trace_default_construction():
    """TouchTrace should be constructable with no arguments using safe defaults."""
    t = TouchTrace()
    assert t.touch_id == 0
    assert t.start_pos == (0.0, 0.0)
    assert t.current_pos == (0.0, 0.0)
    assert t.crossed_strings == []
    assert t.hold_active is False


def test_touch_trace_crossed_strings_is_independent():
    """Each TouchTrace instance should have its own crossed_strings list."""
    t1 = TouchTrace()
    t2 = TouchTrace()
    t1.crossed_strings.append(1)
    assert t2.crossed_strings == [], (
        "crossed_strings lists should not be shared between instances"
    )


def test_touch_trace_field_assignment():
    """TouchTrace fields should accept and return correct values."""
    t = TouchTrace(
        touch_id=42,
        start_pos=(100.0, 200.0),
        current_pos=(150.0, 200.0),
        start_time=1.0,
        current_time=1.2,
        crossed_strings=[0, 1, 2],
        hold_active=False,
    )
    assert t.touch_id == 42
    assert t.start_pos == (100.0, 200.0)
    assert t.crossed_strings == [0, 1, 2]


# ---------------------------------------------------------------------------
# TuningPreset tests
# ---------------------------------------------------------------------------


def test_tuning_preset_default_construction():
    """TuningPreset should be constructable with no arguments using safe defaults."""
    p = TuningPreset()
    assert p.name == ""
    assert p.notes == []
    assert p.frequencies == []


def test_tuning_preset_notes_is_independent():
    """Each TuningPreset instance should have its own notes list."""
    p1 = TuningPreset()
    p2 = TuningPreset()
    p1.notes.append("D2")
    assert p2.notes == [], "notes lists should not be shared between instances"


def test_tuning_preset_field_assignment():
    """TuningPreset fields should accept and return the correct values."""
    notes = ["D2", "E2", "F2", "G2", "A2", "B2", "C3", "D3"]
    freqs = [73.42, 82.41, 87.31, 98.00, 110.00, 123.47, 130.81, 146.83]
    p = TuningPreset(name="Test Preset", notes=notes, frequencies=freqs)
    assert p.name == "Test Preset"
    assert len(p.notes) == 8
    assert p.frequencies[0] == pytest.approx(73.42)
