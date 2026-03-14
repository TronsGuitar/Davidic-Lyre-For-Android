"""
app/lyre_widget.py – Kivy widget that draws the lyre and routes touch events.

The LyreWidget is responsible for:
  - Drawing the wooden body, arms, crossbar and strings on its Canvas.
  - Updating string positions when its size changes.
  - Forwarding touch events to the GestureRecognizer.
  - Running per-frame string vibration animations.
  - Drawing optional note labels.
"""

import time

from kivy.clock import Clock  # type: ignore
from kivy.graphics import (  # type: ignore
    Color,
    Ellipse,
    Line,
    Rectangle,
    RoundedRectangle,
)
from kivy.uix.widget import Widget  # type: ignore

from app.audio_engine import AudioEngine
from app.config import (
    ARM_WIDTH_PX,
    COLORS,
    CROSSBAR_HEIGHT_PX,
    DEFAULT_LABELS_ON,
    DEFAULT_LEFT_HAND,
    NUM_STRINGS,
    RESONATOR_HEIGHT_RATIO,
    RESONATOR_TOP_RATIO,
    STRING_AREA_BOTTOM_RATIO,
    STRING_AREA_TOP_RATIO,
    STRING_HITBOX_HALF_WIDTH_PX,
    STRING_MARGIN_RATIO,
    STRING_THICKNESSES_PX,
    VIBRATION_DECAY,
    VIBRATION_MAX_AMP,
)
from app.gestures import GestureRecognizer
from app.models import LyreString
from app.tuning import DEFAULT_PRESET, TuningPreset


class LyreWidget(Widget):
    """
    The central instrument widget.

    Public API::

        widget.load_preset(preset)   # switch tuning
        widget.set_labels(on: bool)  # toggle note labels
        widget.set_left_hand(on: bool)

    The widget fires audio via an AudioEngine instance which must be
    passed at construction or set via ``widget.audio_engine``.
    """

    def __init__(self, audio_engine: AudioEngine, **kwargs):
        super().__init__(**kwargs)
        self.audio_engine: AudioEngine = audio_engine
        self._preset: TuningPreset = DEFAULT_PRESET
        self._strings: list[LyreString] = []
        self._gesture: GestureRecognizer = GestureRecognizer([])
        self._labels_on: bool = DEFAULT_LABELS_ON
        self._left_hand: bool = DEFAULT_LEFT_HAND

        # Wire gesture callbacks
        self._gesture.on_pluck  = self._on_pluck
        self._gesture.on_mute   = self._on_mute
        self._gesture.on_unmute = self._on_unmute

        self.bind(size=self._rebuild, pos=self._rebuild)

        # Animation clock – 60 fps
        Clock.schedule_interval(self._tick, 1.0 / 60.0)

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def load_preset(self, preset: TuningPreset) -> None:
        """Switch to a new tuning preset."""
        self._preset = preset
        self._rebuild()

    def set_labels(self, on: bool) -> None:
        self._labels_on = on
        self._rebuild()

    def set_left_hand(self, on: bool) -> None:
        self._left_hand = on
        self._rebuild()

    # ------------------------------------------------------------------
    # Geometry helpers
    # ------------------------------------------------------------------

    def _compute_string_positions(self) -> list[LyreString]:
        w, h = self.width, self.height
        if w == 0 or h == 0:
            return []

        margin  = w * STRING_MARGIN_RATIO
        usable  = w - 2 * margin
        spacing = usable / (NUM_STRINGS - 1) if NUM_STRINGS > 1 else usable
        y_top   = h * STRING_AREA_TOP_RATIO + CROSSBAR_HEIGHT_PX
        y_bot   = h * STRING_AREA_BOTTOM_RATIO

        strings: list[LyreString] = []
        for i in range(NUM_STRINGS):
            idx = i if not self._left_hand else (NUM_STRINGS - 1 - i)
            note = self._preset.notes[idx]
            freq = self._preset.frequencies[idx]
            x    = margin + i * spacing + self.x
            th   = STRING_THICKNESSES_PX[idx]

            s = LyreString(
                id=idx,
                note_name=note,
                frequency=freq,
                x=x,
                y_top=y_top + self.y,
                y_bottom=y_bot + self.y,
                thickness_px=th,
                hitbox_width_px=STRING_HITBOX_HALF_WIDTH_PX * 2,
                sample_path=f"lyre_{note.replace('#', 's')}.wav",
            )
            strings.append(s)

        return strings

    # ------------------------------------------------------------------
    # Drawing
    # ------------------------------------------------------------------

    def _rebuild(self, *_args) -> None:
        self._strings = self._compute_string_positions()
        self._gesture = GestureRecognizer(self._strings)
        self._gesture.on_pluck  = self._on_pluck
        self._gesture.on_mute   = self._on_mute
        self._gesture.on_unmute = self._on_unmute
        self._draw()

    def _draw(self) -> None:
        self.canvas.clear()
        w, h = self.width, self.height
        if w == 0 or h == 0:
            return

        with self.canvas:
            self._draw_body(w, h)
            self._draw_strings()
            if self._labels_on:
                self._draw_labels()

    def _draw_body(self, w: float, h: float) -> None:
        """Draw resonator, arms, and crossbar."""
        lw  = COLORS["light_wood"]
        mw  = COLORS["medium_wood"]
        dw  = COLORS["dark_wood"]
        hw  = COLORS["highlight_wear"]

        # --- resonator (rounded lower body) ---
        res_top = h * RESONATOR_TOP_RATIO + self.y
        res_h   = h * RESONATOR_HEIGHT_RATIO
        res_w   = w * 0.70
        res_x   = self.x + (w - res_w) / 2

        Color(*dw)
        RoundedRectangle(
            pos=(res_x, res_top - res_h),
            size=(res_w, res_h),
            radius=[res_w * 0.45, res_w * 0.45, res_w * 0.15, res_w * 0.15],
        )
        Color(*mw)
        RoundedRectangle(
            pos=(res_x + 6, res_top - res_h + 6),
            size=(res_w - 12, res_h - 12),
            radius=[res_w * 0.42, res_w * 0.42, res_w * 0.12, res_w * 0.12],
        )
        # highlight stripe
        Color(*hw)
        Rectangle(
            pos=(res_x + res_w * 0.35, res_top - res_h + 10),
            size=(res_w * 0.08, res_h * 0.55),
        )

        # --- arms (two upright posts) ---
        arm_y_bottom = res_top
        arm_y_top    = h * STRING_AREA_TOP_RATIO + self.y
        arm_h        = arm_y_bottom - arm_y_top

        left_arm_x  = res_x
        right_arm_x = res_x + res_w - ARM_WIDTH_PX

        Color(*dw)
        Rectangle(pos=(left_arm_x,  arm_y_top), size=(ARM_WIDTH_PX, arm_h))
        Rectangle(pos=(right_arm_x, arm_y_top), size=(ARM_WIDTH_PX, arm_h))
        Color(*lw)
        Rectangle(pos=(left_arm_x  + 3, arm_y_top + 4), size=(ARM_WIDTH_PX - 6, arm_h - 8))
        Rectangle(pos=(right_arm_x + 3, arm_y_top + 4), size=(ARM_WIDTH_PX - 6, arm_h - 8))

        # --- crossbar ---
        cross_y = arm_y_top
        Color(*dw)
        Rectangle(pos=(left_arm_x, cross_y), size=(res_w, CROSSBAR_HEIGHT_PX))
        Color(*lw)
        Rectangle(pos=(left_arm_x + 2, cross_y + 3), size=(res_w - 4, CROSSBAR_HEIGHT_PX - 6))

        # --- sound hole on resonator ---
        hole_r = res_w * 0.08
        hole_cx = res_x + res_w / 2
        hole_cy = res_top - res_h * 0.55
        Color(*dw)
        Ellipse(
            pos=(hole_cx - hole_r, hole_cy - hole_r),
            size=(hole_r * 2, hole_r * 2),
        )

    def _draw_strings(self) -> None:
        """Draw each string as a coloured line with vibration offset."""
        for s in self._strings:
            # Colour: lighter/thinner for high strings, darker for low
            t = s.id / (NUM_STRINGS - 1)   # 0 (low) → 1 (high)
            lr = COLORS["gut_string_light"]
            dr = COLORS["gut_string_dark"]
            r = dr[0] + t * (lr[0] - dr[0])
            g = dr[1] + t * (lr[1] - dr[1])
            b = dr[2] + t * (lr[2] - dr[2])
            alpha = 0.4 if s.muted else 1.0

            Color(r, g, b, alpha)

            vib = s.vibration_amp * VIBRATION_MAX_AMP
            # Wavy string: three-point polyline
            mid_y = (s.y_top + s.y_bottom) / 2
            Line(
                points=[
                    s.x, s.y_top,
                    s.x + vib, mid_y,
                    s.x, s.y_bottom,
                ],
                width=s.thickness_px / 2,
                joint="round",
            )

            # Draw knot at crossbar
            Color(*COLORS["dark_wood"])
            Ellipse(
                pos=(s.x - 3, s.y_top - 4),
                size=(6, 6),
            )

    def _draw_labels(self) -> None:
        """Overlay note names near the top of each string."""
        # Labels are drawn via Kivy Label widgets added in _rebuild,
        # but for Canvas simplicity we skip text rendering here.
        # A full implementation would use kivy.graphics.instructions.
        # (Requires a separate Label per string added to the widget tree.)
        pass

    # ------------------------------------------------------------------
    # Touch events
    # ------------------------------------------------------------------

    def on_touch_down(self, touch) -> bool:
        if not self.collide_point(touch.x, touch.y):
            return False
        self._gesture.touch_down(touch.uid, (touch.x, touch.y))
        return True

    def on_touch_move(self, touch) -> bool:
        if touch.uid not in {
            tr.touch_id for tr in self._gesture._traces.values()
        }:
            return False
        self._gesture.touch_move(touch.uid, (touch.x, touch.y))
        return True

    def on_touch_up(self, touch) -> bool:
        if touch.uid not in {
            tr.touch_id for tr in self._gesture._traces.values()
        }:
            return False
        self._gesture.touch_up(touch.uid, (touch.x, touch.y))
        return True

    # ------------------------------------------------------------------
    # Frame tick
    # ------------------------------------------------------------------

    def _tick(self, dt: float) -> None:
        """Advance animation and gesture hold-detection each frame."""
        self._gesture.update()

        changed = False
        for s in self._strings:
            if s.vibration_amp > 0.0:
                s.tick_animation(VIBRATION_DECAY)
                changed = True

        if changed:
            self._draw_strings_only()

    def _draw_strings_only(self) -> None:
        """Redraw only the strings layer for animation performance."""
        # For simplicity, trigger a full redraw; a production app would
        # use a separate canvas group for strings only.
        self._draw()

    # ------------------------------------------------------------------
    # Gesture callbacks
    # ------------------------------------------------------------------

    def _on_pluck(self, string_id: int, velocity: float) -> None:
        for s in self._strings:
            if s.id == string_id:
                s.pluck()
                break
        self.audio_engine.pluck(string_id, velocity)

    def _on_mute(self, string_id: int) -> None:
        for s in self._strings:
            if s.id == string_id:
                s.mute()
                break
        self.audio_engine.mute(string_id)

    def _on_unmute(self, string_id: int) -> None:
        for s in self._strings:
            if s.id == string_id:
                s.unmute()
                break
