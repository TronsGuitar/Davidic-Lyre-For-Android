"""
tests/test_gestures.py – Unit tests for app.gestures module.

All tests are pure Python; no Kivy dependency required.
"""

import time
from unittest.mock import MagicMock

import pytest

from app.gestures import GestureRecognizer, _segment_crosses_hitbox
from app.models import LyreString


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _make_string(
    sid: int,
    x: float,
    y_top: float = 200.0,
    y_bottom: float = 800.0,
    hitbox_width_px: float = 68.0,
) -> LyreString:
    return LyreString(
        id=sid,
        note_name="X",
        frequency=100.0,
        x=x,
        y_top=y_top,
        y_bottom=y_bottom,
        hitbox_width_px=hitbox_width_px,
    )


def _make_eight_strings() -> list[LyreString]:
    """Return 8 strings evenly spaced from x=100 to x=800."""
    return [_make_string(i, 100.0 + i * 100.0) for i in range(8)]


def _make_recognizer(strings: list[LyreString] | None = None) -> GestureRecognizer:
    if strings is None:
        strings = _make_eight_strings()
    gr = GestureRecognizer(strings)
    gr.on_pluck  = MagicMock()
    gr.on_mute   = MagicMock()
    gr.on_unmute = MagicMock()
    return gr


# ---------------------------------------------------------------------------
# _segment_crosses_hitbox
# ---------------------------------------------------------------------------

class TestSegmentCrossesHitbox:
    def test_horizontal_sweep_crosses_string(self):
        s = _make_string(0, x=100.0)
        # Sweep from left (x=50) to right (x=150), at mid-y
        assert _segment_crosses_hitbox((50.0, 500.0), (150.0, 500.0), s)

    def test_sweep_misses_string_on_x(self):
        s = _make_string(0, x=500.0)
        assert not _segment_crosses_hitbox((50.0, 500.0), (150.0, 500.0), s)

    def test_sweep_misses_string_on_y(self):
        s = _make_string(0, x=100.0, y_top=200.0, y_bottom=800.0)
        # Sweep at y=100 (above the string)
        assert not _segment_crosses_hitbox((50.0, 100.0), (150.0, 100.0), s)

    def test_vertical_movement_within_hitbox(self):
        s = _make_string(0, x=100.0)
        # Vertical movement at x=100 (inside hitbox)
        assert _segment_crosses_hitbox((100.0, 100.0), (100.0, 900.0), s)

    def test_diagonal_crosses_string(self):
        s = _make_string(0, x=200.0, y_top=200.0, y_bottom=800.0)
        assert _segment_crosses_hitbox((100.0, 300.0), (300.0, 700.0), s)


# ---------------------------------------------------------------------------
# Tap detection
# ---------------------------------------------------------------------------

class TestTapDetection:
    def test_tap_on_string_fires_pluck(self):
        gr = _make_recognizer()
        t0 = time.monotonic()
        gr.touch_down(1, (100.0, 500.0), t0)
        gr.touch_up(1, (100.0, 500.0), t0 + 0.05)

        gr.on_pluck.assert_called_once()
        call_args = gr.on_pluck.call_args[0]
        assert call_args[0] == 0   # string id 0

    def test_tap_on_empty_space_no_pluck(self):
        gr = _make_recognizer()
        t0 = time.monotonic()
        gr.touch_down(1, (50.0, 500.0), t0)   # x=50, no string there
        gr.touch_up(1, (50.0, 500.0), t0 + 0.05)
        gr.on_pluck.assert_not_called()

    def test_tap_with_large_drift_no_pluck(self):
        gr = _make_recognizer()
        t0 = time.monotonic()
        gr.touch_down(1, (100.0, 500.0), t0)
        # Move far beyond tap drift threshold
        gr.touch_up(1, (200.0, 500.0), t0 + 0.04)
        gr.on_pluck.assert_not_called()

    def test_slow_tap_exceeds_hold_threshold_no_pluck_on_up(self):
        """A touch held beyond the threshold should not produce a tap on release."""
        gr = _make_recognizer()
        t0 = time.monotonic()
        gr.touch_down(1, (100.0, 500.0), t0)
        # Simulate time passing and update() activating hold
        gr.update(t0 + 0.20)     # 200 ms ≥ 150 ms threshold → hold activated
        gr.touch_up(1, (100.0, 500.0), t0 + 0.20)
        # Tap callback must NOT be called; mute should have been called
        gr.on_pluck.assert_not_called()
        gr.on_mute.assert_called_once_with(0)


# ---------------------------------------------------------------------------
# Swipe / strum detection
# ---------------------------------------------------------------------------

class TestSwipeDetection:
    def test_swipe_right_crosses_multiple_strings(self):
        gr = _make_recognizer()
        t0 = time.monotonic()
        gr.touch_down(1, (50.0, 500.0), t0)

        # Move right across strings 0–4 (x=100,200,300,400,500)
        positions = [
            (120.0, 500.0),
            (220.0, 500.0),
            (320.0, 500.0),
            (420.0, 500.0),
            (520.0, 500.0),
        ]
        for x, y in positions:
            gr.touch_move(1, (x, y), t0 + 0.01)

        calls = gr.on_pluck.call_args_list
        plucked_ids = [c[0][0] for c in calls]
        # Should have plucked strings 0, 1, 2, 3, 4 in order
        assert plucked_ids == list(range(5))

    def test_swipe_left_crosses_strings_in_reverse(self):
        gr = _make_recognizer()
        t0 = time.monotonic()
        gr.touch_down(1, (850.0, 500.0), t0)

        # Move left past strings 7..3
        positions = [
            (750.0, 500.0),
            (650.0, 500.0),
            (550.0, 500.0),
            (450.0, 500.0),
            (350.0, 500.0),
        ]
        for x, y in positions:
            gr.touch_move(1, (x, y), t0 + 0.01)

        calls = gr.on_pluck.call_args_list
        plucked_ids = [c[0][0] for c in calls]
        assert plucked_ids == [7, 6, 5, 4, 3]

    def test_no_double_pluck_on_same_string(self):
        gr = _make_recognizer()
        t0 = time.monotonic()
        gr.touch_down(1, (50.0, 500.0), t0)

        # Cross string 0 twice (jitter without leaving hitbox zone)
        gr.touch_move(1, (110.0, 500.0), t0 + 0.01)
        gr.touch_move(1, (105.0, 500.0), t0 + 0.02)
        gr.touch_move(1, (120.0, 500.0), t0 + 0.03)

        plucked_ids = [c[0][0] for c in gr.on_pluck.call_args_list]
        assert plucked_ids.count(0) == 1


# ---------------------------------------------------------------------------
# Hold mute
# ---------------------------------------------------------------------------

class TestHoldMute:
    def test_hold_activates_mute(self):
        gr = _make_recognizer()
        t0 = time.monotonic()
        gr.touch_down(1, (100.0, 500.0), t0)
        gr.update(t0 + 0.20)    # elapsed > 150 ms
        gr.on_mute.assert_called_once_with(0)

    def test_hold_not_activated_too_soon(self):
        gr = _make_recognizer()
        t0 = time.monotonic()
        gr.touch_down(1, (100.0, 500.0), t0)
        gr.update(t0 + 0.05)    # only 50 ms
        gr.on_mute.assert_not_called()

    def test_hold_not_activated_with_too_much_drift(self):
        gr = _make_recognizer()
        t0 = time.monotonic()
        gr.touch_down(1, (100.0, 500.0), t0)
        # Drift by 30 px (> HOLD_DRIFT_PX=22)
        gr.touch_move(1, (130.0, 500.0), t0 + 0.05)
        gr.update(t0 + 0.20)
        gr.on_mute.assert_not_called()

    def test_hold_release_fires_unmute(self):
        gr = _make_recognizer()
        t0 = time.monotonic()
        gr.touch_down(1, (100.0, 500.0), t0)
        gr.update(t0 + 0.20)
        gr.touch_up(1, (100.0, 500.0), t0 + 0.30)
        gr.on_unmute.assert_called_once_with(0)


# ---------------------------------------------------------------------------
# Drag mute
# ---------------------------------------------------------------------------

class TestDragMute:
    def test_drag_mutes_multiple_strings(self):
        gr = _make_recognizer()
        t0 = time.monotonic()
        gr.touch_down(1, (100.0, 500.0), t0)
        # Activate hold on string 0
        gr.update(t0 + 0.20)

        # Drag across string 1, 2
        gr.touch_move(1, (210.0, 500.0), t0 + 0.25)
        gr.touch_move(1, (320.0, 500.0), t0 + 0.30)

        muted_ids = [c[0][0] for c in gr.on_mute.call_args_list]
        assert 0 in muted_ids
        assert 1 in muted_ids
        assert 2 in muted_ids

    def test_drag_mute_no_pluck(self):
        gr = _make_recognizer()
        t0 = time.monotonic()
        gr.touch_down(1, (100.0, 500.0), t0)
        gr.update(t0 + 0.20)   # hold active

        gr.touch_move(1, (210.0, 500.0), t0 + 0.25)
        # During drag-mute, no pluck should fire for newly crossed strings
        gr.on_pluck.assert_not_called()
"""Tests for gesture detection helpers."""

from app.gestures import is_hold, is_swipe, is_tap, strings_crossed, swipe_velocity
from app.models import LyreString


class TestTapDetection:
    def test_small_movement_short_duration_is_tap(self):
        assert is_tap(dx=5, dy=5, duration=0.05) is True

    def test_large_dx_is_not_tap(self):
        assert is_tap(dx=30, dy=0, duration=0.05) is False

    def test_large_dy_is_not_tap(self):
        assert is_tap(dx=0, dy=30, duration=0.05) is False

    def test_long_duration_is_not_tap(self):
        assert is_tap(dx=2, dy=2, duration=0.3) is False

    def test_zero_movement_zero_duration_is_tap(self):
        assert is_tap(dx=0, dy=0, duration=0.0) is True


class TestHoldDetection:
    def test_long_hold_detected(self):
        assert is_hold(dx=0, dy=0, duration=0.2) is True

    def test_short_hold_not_detected(self):
        assert is_hold(dx=0, dy=0, duration=0.1) is False

    def test_exact_threshold_is_hold(self):
        assert is_hold(dx=5, dy=5, duration=0.15) is True


class TestSwipeDetection:
    def test_large_movement_is_swipe(self):
        assert is_swipe(dx=30, dy=0) is True

    def test_small_movement_is_not_swipe(self):
        assert is_swipe(dx=5, dy=5) is False

    def test_diagonal_swipe(self):
        assert is_swipe(dx=20, dy=20) is True

    def test_exact_threshold(self):
        assert is_swipe(dx=25, dy=0) is True


class TestSwipeVelocity:
    def test_minimum_velocity(self):
        assert swipe_velocity(0) == 0.6

    def test_maximum_velocity_clamped(self):
        assert swipe_velocity(1000) == 2.0

    def test_mid_velocity(self):
        v = swipe_velocity(35)
        assert 0.9 < v < 1.1  # approx 1.0


class TestStringsCrossed:
    @staticmethod
    def _make_strings():
        return [
            LyreString(idx=i, note=f"S{i}", frequency=100 + i * 10,
                        thickness=3.0, x=100 + i * 50,
                        y_top=500, y_bottom=100)
            for i in range(4)
        ]

    def test_crossing_one_string(self):
        strings = self._make_strings()
        # Swipe from x=90 to x=110 only crosses the string at x=100
        result = strings_crossed(90, 300, 110, 300, strings)
        assert len(result) == 1
        assert result[0].idx == 0

    def test_crossing_multiple_strings(self):
        strings = self._make_strings()
        result = strings_crossed(90, 300, 310, 300, strings)
        assert len(result) >= 3

    def test_no_crossing(self):
        strings = self._make_strings()
        result = strings_crossed(10, 300, 50, 300, strings)
        assert len(result) == 0

    def test_y_outside_range_excluded(self):
        strings = self._make_strings()
        result = strings_crossed(90, 600, 310, 600, strings)
        assert len(result) == 0
