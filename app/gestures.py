"""
app/gestures.py – Pure-Python gesture recognition for the Davidic Lyre.

The GestureRecognizer holds a dictionary of active TouchTrace objects.
Callers feed it raw touch events; it fires callbacks for tap, swipe,
hold-mute, and drag-mute gestures.

All spatial parameters come from app.config so they can be tuned centrally.
"""

import time
from typing import Callable, Dict, List, Optional, Tuple

from app.config import (
    HOLD_DRIFT_PX,
    HOLD_THRESHOLD_MS,
    MIN_SWIPE_PX,
    TAP_DRIFT_PX,
)
from app.models import LyreString, TouchTrace


# ---------------------------------------------------------------------------
# Type aliases for callbacks
# ---------------------------------------------------------------------------
PluckCallback = Callable[[int, float], None]    # (string_id, velocity)
MuteCallback  = Callable[[int], None]           # (string_id,)
UnmuteCallback = Callable[[int], None]          # (string_id,)


def _segment_crosses_hitbox(
    p0: Tuple[float, float],
    p1: Tuple[float, float],
    string: LyreString,
) -> bool:
    """
    Return True when the line segment p0→p1 crosses *string*'s hitbox.

    The hitbox is a vertical band (x-range) that spans the full height
    of the string.  We parameterise the segment and check whether the
    x-crossing of the band boundary occurs within the y-range of the
    string.
    """
    x0, y0 = p0
    x1, y1 = p1
    dx = x1 - x0
    dy = y1 - y0

    left  = string.hitbox_left
    right = string.hitbox_right
    ymin  = string.y_top
    ymax  = string.y_bottom

    # Quick bounding-box rejection
    xmin_seg = min(x0, x1)
    xmax_seg = max(x0, x1)
    if xmax_seg < left or xmin_seg > right:
        return False

    # Check whether the segment passes through the hitbox band
    if abs(dx) < 1e-6:
        # Vertical movement – just check x overlap with hitbox
        if left <= x0 <= right:
            return min(y0, y1) <= ymax and max(y0, y1) >= ymin
        return False

    # Find t at which segment crosses left and right boundaries
    t_left  = (left  - x0) / dx
    t_right = (right - x0) / dx
    t_enter = max(0.0, min(t_left, t_right))
    t_exit  = min(1.0, max(t_left, t_right))

    if t_enter > t_exit:
        return False

    # y-value at the middle of the crossing interval
    t_mid = (t_enter + t_exit) / 2
    y_mid = y0 + t_mid * dy
    return ymin <= y_mid <= ymax


def _crossing_t(
    p0: Tuple[float, float],
    p1: Tuple[float, float],
    string: LyreString,
) -> float:
    """
    Return the parametric t (0–1) at which the segment p0→p1 crosses
    the centre of *string*'s hitbox.  Used to order crossing events.
    """
    x0, _ = p0
    x1, _ = p1
    dx = x1 - x0
    if abs(dx) < 1e-6:
        return 0.0
    return (string.x - x0) / dx


class GestureRecognizer:
    """
    Stateful gesture processor for multi-touch lyre interaction.

    Usage::

        gr = GestureRecognizer(strings)
        gr.on_pluck  = lambda sid, vel: play(sid, vel)
        gr.on_mute   = lambda sid: mute(sid)
        gr.on_unmute = lambda sid: unmute(sid)

        # In your touch handlers:
        gr.touch_down(touch_id, (x, y), t)
        gr.touch_move(touch_id, (x, y), t)
        gr.touch_up(touch_id, (x, y), t)

        # Call once per frame to detect hold-mutes:
        gr.update(current_time)
    """

    def __init__(self, strings: List[LyreString]) -> None:
        self.strings: List[LyreString] = strings

        # Mutable thresholds (can be overridden by UI controls)
        self.hold_threshold_ms: float = HOLD_THRESHOLD_MS
        self.tap_drift_px:      float = TAP_DRIFT_PX
        self.hold_drift_px:     float = HOLD_DRIFT_PX
        self.min_swipe_px:      float = MIN_SWIPE_PX

        # Active traces keyed by touch_id
        self._traces: Dict[int, TouchTrace] = {}

        # Callbacks (set by caller)
        self.on_pluck:  Optional[PluckCallback]  = None
        self.on_mute:   Optional[MuteCallback]   = None
        self.on_unmute: Optional[UnmuteCallback] = None

    # ------------------------------------------------------------------
    # Public event entry points
    # ------------------------------------------------------------------

    def touch_down(
        self,
        touch_id: int,
        pos: Tuple[float, float],
        t: Optional[float] = None,
    ) -> None:
        """Register a new finger contact."""
        if t is None:
            t = time.monotonic()
        trace = TouchTrace(
            touch_id=touch_id,
            start_pos=pos,
            current_pos=pos,
            start_time=t,
            current_time=t,
        )
        # Record which string (if any) was touched initially
        sid = self._string_at(pos)
        if sid is not None:
            trace.crossed_strings.append(sid)
        self._traces[touch_id] = trace

    def touch_move(
        self,
        touch_id: int,
        pos: Tuple[float, float],
        t: Optional[float] = None,
    ) -> None:
        """Update an active contact and detect swipe crossings."""
        if touch_id not in self._traces:
            return
        if t is None:
            t = time.monotonic()

        trace = self._traces[touch_id]
        prev_pos = trace.current_pos
        trace.update(pos, t)

        # If a hold is already active, check drag-mute crossings
        if trace.hold_active:
            self._check_drag_mute(trace, prev_pos, pos)
            return

        # Detect swipe crossings only if movement exceeds threshold
        dist = trace.distance
        if dist >= self.min_swipe_px:
            self._check_swipe_crossings(trace, prev_pos, pos)

    def touch_up(
        self,
        touch_id: int,
        pos: Tuple[float, float],
        t: Optional[float] = None,
    ) -> None:
        """Handle finger lift: fire tap or clean up hold."""
        if touch_id not in self._traces:
            return
        if t is None:
            t = time.monotonic()

        trace = self._traces.pop(touch_id)
        trace.update(pos, t)

        # If a hold was active, release mute on the hold-muted string
        if trace.hold_active:
            # Unmute all strings muted by this trace
            for sid in trace.crossed_strings:
                if self.on_unmute:
                    self.on_unmute(sid)
            return

        # Detect tap: small drift, short duration, no prior crossings via swipe
        if (
            trace.distance <= self.tap_drift_px
            and trace.elapsed_ms < self.hold_threshold_ms
        ):
            sid = self._string_at(trace.start_pos)
            if sid is not None:
                velocity = min(1.0, trace.elapsed_ms / 80.0)  # proxy
                if self.on_pluck:
                    self.on_pluck(sid, velocity)

    def update(self, t: Optional[float] = None) -> None:
        """
        Call once per frame.  Promotes qualifying stationary touches
        to hold-mute state.
        """
        if t is None:
            t = time.monotonic()

        for trace in self._traces.values():
            if trace.hold_active:
                continue
            trace.current_time = t
            if (
                trace.elapsed_ms >= self.hold_threshold_ms
                and trace.distance <= self.hold_drift_px
                and trace.crossed_strings
            ):
                trace.hold_active = True
                # Mute the string touched at the start
                sid = trace.crossed_strings[0]
                if self.on_mute:
                    self.on_mute(sid)

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    def _string_at(self, pos: Tuple[float, float]) -> Optional[int]:
        """Return the id of the string whose hitbox contains *pos*, or None."""
        for s in self.strings:
            if s.contains_point(pos[0], pos[1]):
                return s.id
        return None

    def _check_swipe_crossings(
        self,
        trace: TouchTrace,
        p0: Tuple[float, float],
        p1: Tuple[float, float],
    ) -> None:
        """
        Detect all string hitboxes crossed by the segment p0→p1 and fire
        pluck events in crossing order (not already crossed).
        """
        newly_crossed: List[Tuple[float, int]] = []
        for s in self.strings:
            if s.id in trace.crossed_strings:
                continue
            if _segment_crosses_hitbox(p0, p1, s):
                t_val = _crossing_t(p0, p1, s)
                newly_crossed.append((t_val, s.id))

        # Sort by position along movement vector
        newly_crossed.sort(key=lambda item: item[0])

        for _, sid in newly_crossed:
            trace.crossed_strings.append(sid)
            if self.on_pluck:
                # Estimate velocity from movement speed
                dx = p1[0] - p0[0]
                dy = p1[1] - p0[1]
                speed = (dx * dx + dy * dy) ** 0.5
                velocity = min(1.0, speed / 200.0)
                self.on_pluck(sid, velocity)

    def _check_drag_mute(
        self,
        trace: TouchTrace,
        p0: Tuple[float, float],
        p1: Tuple[float, float],
    ) -> None:
        """Mute any strings newly crossed while a hold is active."""
        for s in self.strings:
            if s.id in trace.crossed_strings:
                continue
            if _segment_crosses_hitbox(p0, p1, s):
                trace.crossed_strings.append(s.id)
                if self.on_mute:
                    self.on_mute(s.id)
