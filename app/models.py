"""
app/models.py — Data model classes for the Davidic Lyre app.

Defines the core data structures used throughout the application:
  - LyreString  — represents one physical string on the instrument
  - TouchTrace  — tracks the lifecycle of a single touch event
  - TuningPreset — encapsulates a named set of string notes and frequencies

Field definitions follow PRD Section 15.
"""

from dataclasses import dataclass, field
from typing import List, Tuple


@dataclass
class LyreString:
    """Represents one string on the lyre instrument.

    Stores both the musical properties (note, frequency, sample path) and the
    on-screen layout properties (position, hitbox dimensions) for a single string.

    Attributes:
        id: Zero-based index identifying the string (0 = lowest/leftmost).
        note_name: Human-readable note name, e.g. ``"D2"``.
        frequency: Fundamental frequency in Hz.
        x: Horizontal centre position of the string on screen (pixels).
        y_top: Y-coordinate of the top anchor point of the string (pixels).
        y_bottom: Y-coordinate of the bottom anchor point of the string (pixels).
        thickness_px: Visual thickness of the string drawn on canvas (pixels).
        hitbox_width_px: Width of the invisible touch-sensitive region around
            the string (pixels).  Should be wider than *thickness_px* to make
            the string easy to tap.
        muted: Whether the string is currently muted by a held finger.
        ringing: Whether the string is currently producing sound.
        gain: Per-string gain multiplier (0.0–1.0).
        sample_path: Filesystem path to the WAV sample for this string.
    """

    id: int = 0
    note_name: str = ""
    frequency: float = 0.0
    x: float = 0.0
    y_top: float = 0.0
    y_bottom: float = 0.0
    thickness_px: float = 2.0
    hitbox_width_px: float = 40.0
    muted: bool = False
    ringing: bool = False
    gain: float = 1.0
    sample_path: str = ""

    # TODO: Add animation state fields (oscillation amplitude, phase) in Phase 1


@dataclass
class TouchTrace:
    """Tracks the full lifecycle of a single touch contact on the screen.

    Used by the gesture recogniser (app/gestures.py) to classify a touch as
    a tap, swipe, hold, or drag-mute.  A new ``TouchTrace`` is created on
    every ``on_touch_down`` event and updated through ``on_touch_move`` and
    ``on_touch_up``.

    Attributes:
        touch_id: Unique identifier assigned by Kivy to the touch event.
        start_pos: Screen coordinates ``(x, y)`` where the touch began.
        current_pos: Most recent screen coordinates of the touch.
        start_time: Timestamp (seconds) when the touch was first registered.
        current_time: Timestamp (seconds) of the most recent touch update.
        crossed_strings: Ordered list of string IDs crossed by the touch so
            far (used for swipe strumming).
        hold_active: ``True`` once the hold-mute threshold has been reached.
    """

    touch_id: int = 0
    start_pos: Tuple[float, float] = (0.0, 0.0)
    current_pos: Tuple[float, float] = (0.0, 0.0)
    start_time: float = 0.0
    current_time: float = 0.0
    crossed_strings: List[int] = field(default_factory=list)
    hold_active: bool = False

    # TODO: Add velocity tracking for dynamic pluck volume (Phase 1)


@dataclass
class TuningPreset:
    """A named collection of note names and their target frequencies.

    Attributes:
        name: Human-readable preset name shown in the UI dropdown.
        notes: Ordered list of note-name strings, one per string (lowest first).
        frequencies: Ordered list of frequencies in Hz, matching *notes*.
    """

    name: str = ""
    notes: List[str] = field(default_factory=list)
    frequencies: List[float] = field(default_factory=list)

    # TODO: Add validation that len(notes) == len(frequencies) == 8 (Phase 1)
