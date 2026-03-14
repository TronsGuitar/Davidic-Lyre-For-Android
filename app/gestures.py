"""Gesture detection helpers: tap, swipe, and hold classification."""

from __future__ import annotations

from app.config import (
    HOLD_THRESHOLD,
    MIN_SWIPE_DISTANCE,
    TAP_DRIFT_TOLERANCE,
    MIN_VELOCITY,
    MAX_VELOCITY,
    VELOCITY_DIVISOR,
)
from app.models import LyreString


def is_tap(dx: float, dy: float, duration: float) -> bool:
    """Return ``True`` if the touch movement is within tap tolerances."""
    return (abs(dx) <= TAP_DRIFT_TOLERANCE
            and abs(dy) <= TAP_DRIFT_TOLERANCE
            and duration < HOLD_THRESHOLD)


def is_hold(dx: float, dy: float, duration: float) -> bool:
    """Return ``True`` if the touch qualifies as a hold-mute gesture."""
    return duration >= HOLD_THRESHOLD


def is_swipe(dx: float, dy: float) -> bool:
    """Return ``True`` if the movement distance qualifies as a swipe."""
    return (dx * dx + dy * dy) ** 0.5 >= MIN_SWIPE_DISTANCE


def swipe_velocity(dx: float) -> float:
    """Map a horizontal pixel delta to a pluck velocity."""
    return max(MIN_VELOCITY, min(MAX_VELOCITY, abs(dx) / VELOCITY_DIVISOR))


def strings_crossed(
    prev_x: float,
    prev_y: float,
    cur_x: float,
    cur_y: float,
    strings: list[LyreString],
) -> list[LyreString]:
    """Return strings whose x-position was crossed between two touch points.

    Only strings whose vertical span contains at least one of the y-coordinates
    are considered.
    """
    crossed: list[LyreString] = []
    for s in strings:
        x_between = (prev_x <= s.x <= cur_x) or (cur_x <= s.x <= prev_x)
        y_in_range = s.y_bottom <= cur_y <= s.y_top or s.y_bottom <= prev_y <= s.y_top
        if x_between and y_in_range:
            crossed.append(s)
    # Order by crossing position along the movement vector
    crossed.sort(key=lambda s: abs(s.x - prev_x))
    return crossed
