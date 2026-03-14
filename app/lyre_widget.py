"""Kivy widget that renders the lyre and handles touch events."""

from __future__ import annotations

import time
from math import sin

from kivy.clock import Clock
from kivy.graphics import Color, Line, Rectangle
from kivy.uix.widget import Widget

from app.audio_engine import AudioEngine
from app.config import (
    ARM_WIDTH,
    COLOR_ARM,
    COLOR_BODY,
    COLOR_STRING,
    COLOR_STRING_MUTED,
    CROSSBAR_WIDTH,
    FRAME_BOTTOM_H,
    FRAME_BOTTOM_Y,
    FRAME_LEFT_X_BOTTOM,
    FRAME_LEFT_X_TOP,
    FRAME_RIGHT_X_BOTTOM,
    FRAME_RIGHT_X_TOP,
    HOLD_THRESHOLD,
    STRING_BOTTOM,
    STRING_LEFT,
    STRING_RIGHT,
    STRING_THICKNESSES,
    STRING_TOP,
    TARGET_FPS,
    VIBRATION_BASE,
    VIBRATION_DECAY,
    VIBRATION_FREQ,
    VIBRATION_MAX,
    VIBRATION_MIN,
)
from app.gestures import strings_crossed, swipe_velocity
from app.models import LyreString


class LyreWidget(Widget):
    """Main instrument widget: draws the lyre body and strings and routes
    touch events to the gesture / audio layer."""

    def __init__(self, audio_engine: AudioEngine | None = None, **kwargs):
        super().__init__(**kwargs)
        self.audio_engine = audio_engine or AudioEngine()
        self.strings: list[LyreString] = []
        self.touch_state: dict[int, dict] = {}
        Clock.schedule_interval(self._update_frame, 1 / TARGET_FPS)

    # --- String Management -------------------------------------------------

    def set_strings(self, notes: list[str], frequencies: list[float]) -> None:
        """Create ``LyreString`` objects for the given tuning."""
        self.strings = [
            LyreString(
                idx=i,
                note=note,
                frequency=freq,
                thickness=STRING_THICKNESSES[i] if i < len(STRING_THICKNESSES) else 2.0,
            )
            for i, (note, freq) in enumerate(zip(notes, frequencies))
        ]
        self._layout_strings()

    # --- Layout ------------------------------------------------------------

    def _layout_strings(self) -> None:
        left = self.x + self.width * STRING_LEFT
        right = self.x + self.width * STRING_RIGHT
        top = self.y + self.height * STRING_TOP
        bottom = self.y + self.height * STRING_BOTTOM

        n = len(self.strings)
        for i, s in enumerate(self.strings):
            t = i / (n - 1) if n > 1 else 0.5
            s.x = left + (right - left) * t
            s.y_top = top
            s.y_bottom = bottom

    def on_size(self, *_args):
        self._layout_strings()
        self._redraw()

    def on_pos(self, *_args):
        self._layout_strings()
        self._redraw()

    # --- Drawing -----------------------------------------------------------

    def _redraw(self) -> None:
        self.canvas.clear()
        with self.canvas:
            # Lower resonator body
            Color(*COLOR_BODY)
            Rectangle(
                pos=(self.x + self.width * STRING_LEFT - self.width * 0.03,
                     self.y + self.height * FRAME_BOTTOM_Y),
                size=(self.width * (STRING_RIGHT - STRING_LEFT + 0.06),
                      self.height * FRAME_BOTTOM_H),
            )

            # Arms
            Color(*COLOR_ARM)
            Line(points=[
                self.x + self.width * FRAME_LEFT_X_BOTTOM,
                self.y + self.height * FRAME_BOTTOM_Y + self.height * FRAME_BOTTOM_H,
                self.x + self.width * FRAME_LEFT_X_TOP,
                self.y + self.height * STRING_TOP,
            ], width=ARM_WIDTH)
            Line(points=[
                self.x + self.width * FRAME_RIGHT_X_BOTTOM,
                self.y + self.height * FRAME_BOTTOM_Y + self.height * FRAME_BOTTOM_H,
                self.x + self.width * FRAME_RIGHT_X_TOP,
                self.y + self.height * STRING_TOP,
            ], width=ARM_WIDTH)

            # Crossbar
            Line(points=[
                self.x + self.width * FRAME_LEFT_X_TOP,
                self.y + self.height * STRING_TOP,
                self.x + self.width * FRAME_RIGHT_X_TOP,
                self.y + self.height * STRING_TOP,
            ], width=CROSSBAR_WIDTH)

            # Strings
            now = time.time()
            for s in self.strings:
                age = now - s.last_plucked
                amp = max(0.0, s.vibration * (1.0 - age * VIBRATION_DECAY))
                offset = sin(age * VIBRATION_FREQ) * amp if amp > 0 else 0
                if s.muted:
                    Color(*COLOR_STRING_MUTED)
                else:
                    Color(*COLOR_STRING)
                Line(
                    points=[s.x + offset, s.y_top, s.x + offset, s.y_bottom],
                    width=s.thickness,
                )

    # --- Hit Testing -------------------------------------------------------

    def find_string(self, x: float, y: float) -> LyreString | None:
        """Return the nearest string within hitbox range, or ``None``."""
        best: LyreString | None = None
        best_dist = 999999.0
        for s in self.strings:
            if s.y_bottom <= y <= s.y_top:
                dist = abs(x - s.x)
                if dist < s.hitbox_width and dist < best_dist:
                    best = s
                    best_dist = dist
        return best

    # --- Pluck / Mute ------------------------------------------------------

    def pluck_string(self, s: LyreString, velocity: float = 1.0) -> None:
        """Trigger a pluck on *s* unless it is muted."""
        if s.muted:
            return
        s.last_plucked = time.time()
        s.vibration = max(VIBRATION_MIN, min(VIBRATION_MAX, VIBRATION_BASE * velocity))
        s.ringing = True
        self.audio_engine.play(s.note, velocity)

    def mute_string(self, s: LyreString) -> None:
        s.muted = True
        s.vibration = 1.0
        s.ringing = False
        self.audio_engine.stop(s.note)

    def unmute_string(self, s: LyreString) -> None:
        s.muted = False

    # --- Touch Events ------------------------------------------------------

    def on_touch_down(self, touch):
        if not self.collide_point(*touch.pos):
            return super().on_touch_down(touch)

        s = self.find_string(*touch.pos)
        self.touch_state[touch.uid] = {
            "start": touch.pos,
            "last": touch.pos,
            "time": time.time(),
            "crossed": set(),
            "string": s,
            "hold_active": False,
        }

        if s:
            self.pluck_string(s, velocity=1.0)
            self.touch_state[touch.uid]["crossed"].add(s.idx)
            return True

        return super().on_touch_down(touch)

    def on_touch_move(self, touch):
        state = self.touch_state.get(touch.uid)
        if not state:
            return super().on_touch_move(touch)

        px, py = state["last"]
        cx, cy = touch.pos

        # Strum detection
        for hit in strings_crossed(px, py, cx, cy, self.strings):
            if hit.idx not in state["crossed"]:
                self.pluck_string(hit, velocity=swipe_velocity(cx - px))
                state["crossed"].add(hit.idx)

        # Hold mute detection
        held_time = time.time() - state["time"]
        s = self.find_string(*touch.pos)
        if s and held_time > HOLD_THRESHOLD:
            self.mute_string(s)
            state["hold_active"] = True
            state["string"] = s

        state["last"] = touch.pos
        return True

    def on_touch_up(self, touch):
        state = self.touch_state.pop(touch.uid, None)
        if state and state["hold_active"] and state["string"]:
            self.unmute_string(state["string"])
            return True
        return super().on_touch_up(touch)

    # --- Frame Update ------------------------------------------------------

    def _update_frame(self, _dt: float) -> None:
        self._redraw()
