"""
app/gestures.py — Swipe detection, hold threshold tracking, segment and hitbox
crossing detection for the Davidic Lyre app.

Implements the gesture-recognition algorithms described in PRD Section 16:
  - Tap detection   — touch down + release before hold threshold with minimal drift
  - Hold detection  — touch remains within hold radius past the mute threshold
  - Swipe detection — moving touch crossing string hitboxes in sequence
  - Drag-mute       — hold + drag muting additional strings

This module is intentionally UI-framework-agnostic; it operates on raw position
and timing data so that it can be unit-tested without a running Kivy environment.
"""

from typing import List, Optional, Tuple

from app.config import (
    HOLD_DRIFT_PX,
    MIN_SWIPE_PX,
    MUTE_THRESHOLD_MS,
    TAP_DRIFT_PX,
)
from app.models import LyreString, TouchTrace


# ---------------------------------------------------------------------------
# Tap detection (PRD Section 16)
# ---------------------------------------------------------------------------


def is_tap(trace: TouchTrace, release_time: float) -> bool:
    """Return ``True`` if *trace* qualifies as a tap gesture.

    A tap is detected when:
    - Total finger drift stays below :data:`~app.config.TAP_DRIFT_PX`, AND
    - The touch is released before the hold threshold
      (:data:`~app.config.MUTE_THRESHOLD_MS`).

    Args:
        trace: The ``TouchTrace`` for the touch being evaluated.
        release_time: Timestamp (seconds) when the finger was lifted.

    Returns:
        ``True`` if the touch should be classified as a tap.
    """
    # TODO: Implement tap detection algorithm (Phase 1)
    # held_ms = (release_time - trace.start_time) * 1000
    # drift = _distance(trace.start_pos, trace.current_pos)
    # return drift < TAP_DRIFT_PX and held_ms < MUTE_THRESHOLD_MS
    raise NotImplementedError("Tap detection not yet implemented")


# ---------------------------------------------------------------------------
# Hold detection (PRD Section 16)
# ---------------------------------------------------------------------------


def check_hold(trace: TouchTrace, current_time: float) -> bool:
    """Return ``True`` if the touch has been held long enough to activate mute.

    Args:
        trace: The ``TouchTrace`` being evaluated.
        current_time: Current timestamp in seconds.

    Returns:
        ``True`` if the touch qualifies as a hold-mute activation.
    """
    # TODO: Implement hold detection algorithm (Phase 1)
    # held_ms = (current_time - trace.start_time) * 1000
    # drift = _distance(trace.start_pos, trace.current_pos)
    # return held_ms >= MUTE_THRESHOLD_MS and drift < HOLD_DRIFT_PX
    raise NotImplementedError("Hold detection not yet implemented")


# ---------------------------------------------------------------------------
# Swipe / string-crossing detection (PRD Section 16)
# ---------------------------------------------------------------------------


def find_crossed_strings(
    strings: List[LyreString],
    prev_pos: Tuple[float, float],
    curr_pos: Tuple[float, float],
) -> List[int]:
    """Return IDs of strings whose hitboxes are crossed by the movement segment.

    Examines the line segment from *prev_pos* to *curr_pos* and returns the
    IDs of any ``LyreString`` hitboxes it intersects, ordered by crossing
    position along the movement vector.

    Args:
        strings: The full list of ``LyreString`` objects for the current preset.
        prev_pos: Starting position of the movement segment ``(x, y)``.
        curr_pos: Ending position of the movement segment ``(x, y)``.

    Returns:
        Ordered list of string IDs that were crossed.
    """
    # TODO: Implement segment-hitbox crossing detection (Phase 1)
    # Algorithm:
    #   1. For each string, compute the string's hitbox x-interval
    #      [string.x - hitbox_width_px/2, string.x + hitbox_width_px/2]
    #   2. Check whether the segment's x-extent overlaps that interval
    #   3. Verify the y-extent of the segment falls within [y_top, y_bottom]
    #   4. Sort crossed strings by x-position along the movement direction
    raise NotImplementedError("String crossing detection not yet implemented")


def get_swipe_velocity(
    prev_pos: Tuple[float, float],
    curr_pos: Tuple[float, float],
    delta_time: float,
) -> float:
    """Return the swipe speed in pixels per second.

    Args:
        prev_pos: Position at start of the time interval.
        curr_pos: Position at end of the time interval.
        delta_time: Elapsed time in seconds.

    Returns:
        Speed in px/s, or 0.0 if *delta_time* is non-positive.
    """
    # TODO: Implement swipe velocity calculation (Phase 1)
    raise NotImplementedError("Swipe velocity not yet implemented")


# ---------------------------------------------------------------------------
# Nearest string lookup
# ---------------------------------------------------------------------------


def nearest_string(
    strings: List[LyreString],
    pos: Tuple[float, float],
) -> Optional[LyreString]:
    """Return the ``LyreString`` whose hitbox is closest to *pos*.

    Args:
        strings: List of ``LyreString`` objects.
        pos: Touch position ``(x, y)``.

    Returns:
        The closest ``LyreString``, or ``None`` if *strings* is empty.
    """
    # TODO: Implement nearest-string lookup using hitbox distance (Phase 1)
    raise NotImplementedError("Nearest string lookup not yet implemented")


# ---------------------------------------------------------------------------
# Private helpers
# ---------------------------------------------------------------------------


def _distance(a: Tuple[float, float], b: Tuple[float, float]) -> float:
    """Euclidean distance between two points."""
    return ((b[0] - a[0]) ** 2 + (b[1] - a[1]) ** 2) ** 0.5
