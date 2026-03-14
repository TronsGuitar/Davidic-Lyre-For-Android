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
