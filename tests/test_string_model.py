"""
tests/test_string_model.py – Unit tests for app.models module.

Pure-Python tests; no Kivy dependency.
"""

import pytest

from app.models import LyreString, TouchTrace


class TestLyreString:
    def _make_string(self, **kwargs) -> LyreString:
        defaults = dict(
            id=0,
            note_name="D2",
            frequency=73.42,
            x=100.0,
            y_top=200.0,
            y_bottom=800.0,
            thickness_px=6.0,
            hitbox_width_px=68.0,
        )
        defaults.update(kwargs)
        return LyreString(**defaults)

    # --- hitbox geometry ---

    def test_hitbox_left(self):
        s = self._make_string(x=100.0, hitbox_width_px=68.0)
        assert abs(s.hitbox_left - 66.0) < 0.001

    def test_hitbox_right(self):
        s = self._make_string(x=100.0, hitbox_width_px=68.0)
        assert abs(s.hitbox_right - 134.0) < 0.001

    def test_contains_point_inside(self):
        s = self._make_string(x=100.0, y_top=200.0, y_bottom=800.0, hitbox_width_px=68.0)
        assert s.contains_point(100.0, 500.0)

    def test_contains_point_on_left_edge(self):
        s = self._make_string(x=100.0, hitbox_width_px=68.0, y_top=200.0, y_bottom=800.0)
        assert s.contains_point(66.0, 500.0)

    def test_contains_point_outside_x(self):
        s = self._make_string(x=100.0, hitbox_width_px=68.0, y_top=200.0, y_bottom=800.0)
        assert not s.contains_point(200.0, 500.0)

    def test_contains_point_outside_y(self):
        s = self._make_string(x=100.0, hitbox_width_px=68.0, y_top=200.0, y_bottom=800.0)
        assert not s.contains_point(100.0, 100.0)

    # --- state transitions ---

    def test_initial_state_not_muted_not_ringing(self):
        s = self._make_string()
        assert not s.muted
        assert not s.ringing

    def test_pluck_sets_ringing(self):
        s = self._make_string()
        s.pluck()
        assert s.ringing
        assert not s.muted
        assert s.vibration_amp == 1.0

    def test_mute_clears_ringing(self):
        s = self._make_string()
        s.pluck()
        s.mute()
        assert s.muted
        assert not s.ringing
        assert s.vibration_amp == 0.0

    def test_unmute_clears_muted(self):
        s = self._make_string()
        s.mute()
        s.unmute()
        assert not s.muted

    def test_tick_decays_vibration(self):
        s = self._make_string()
        s.pluck()
        before = s.vibration_amp
        s.tick_animation(decay=0.5)
        assert s.vibration_amp == before * 0.5

    def test_tick_clears_ringing_when_amplitude_negligible(self):
        s = self._make_string()
        s.pluck()
        # Force vibration to tiny value
        s.vibration_amp = 0.005
        s.tick_animation(decay=0.92)
        assert not s.ringing
        assert s.vibration_amp == 0.0


class TestTouchTrace:
    def _make_trace(self, **kwargs) -> TouchTrace:
        defaults = dict(
            touch_id=1,
            start_pos=(50.0, 300.0),
            current_pos=(50.0, 300.0),
            start_time=0.0,
            current_time=0.0,
        )
        defaults.update(kwargs)
        return TouchTrace(**defaults)

    def test_delta_zero_at_start(self):
        trace = self._make_trace()
        assert trace.delta == (0.0, 0.0)

    def test_delta_after_move(self):
        trace = self._make_trace(current_pos=(80.0, 350.0))
        dx, dy = trace.delta
        assert abs(dx - 30.0) < 0.001
        assert abs(dy - 50.0) < 0.001

    def test_distance(self):
        trace = self._make_trace(current_pos=(53.0, 304.0))  # 3,4 right triangle
        assert abs(trace.distance - 5.0) < 0.001

    def test_elapsed_ms(self):
        trace = self._make_trace(start_time=0.0, current_time=0.200)
        assert abs(trace.elapsed_ms - 200.0) < 0.001

    def test_update_changes_position_and_time(self):
        trace = self._make_trace()
        trace.update((120.0, 400.0), 0.5)
        assert trace.current_pos == (120.0, 400.0)
        assert trace.current_time == 0.5
        assert abs(trace.distance - ((70**2 + 100**2) ** 0.5)) < 0.01

    def test_crossed_strings_default_empty(self):
        trace = self._make_trace()
        assert trace.crossed_strings == []

    def test_hold_active_default_false(self):
        trace = self._make_trace()
        assert not trace.hold_active
