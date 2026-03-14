"""
app/models.py – Core data models: LyreString, TouchTrace.

These classes are pure Python (no Kivy dependency) so they can be
instantiated and tested independently of the UI runtime.
"""

from dataclasses import dataclass, field
from typing import List, Tuple


@dataclass
class LyreString:
    """
    Represents one physical string on the lyre.

    Coordinates (x, y_top, y_bottom) are in widget-local pixels.
    The hitbox extends ±hitbox_width_px/2 around *x*.
    """
    id: int                  # 0 = lowest, 7 = highest
    note_name: str
    frequency: float         # Hz
    x: float = 0.0          # horizontal centre in widget pixels
    y_top: float = 0.0      # upper attachment point (crossbar side)
    y_bottom: float = 0.0   # lower attachment point (resonator side)
    thickness_px: float = 4.0
    hitbox_width_px: float = 68.0   # total hitbox width (±34 px)
    muted: bool = False
    ringing: bool = False
    gain: float = 1.0
    sample_path: str = ""

    # --- runtime animation state (not serialised) ---
    vibration_amp: float = 0.0   # current side-to-side displacement (px)

    @property
    def hitbox_left(self) -> float:
        return self.x - self.hitbox_width_px / 2

    @property
    def hitbox_right(self) -> float:
        return self.x + self.hitbox_width_px / 2

    def contains_point(self, px: float, py: float) -> bool:
        """
        Return True when the point (px, py) falls within this string's
        hitbox rectangle.
        """
        return (
            self.hitbox_left <= px <= self.hitbox_right
            and self.y_top <= py <= self.y_bottom
        )

    def mute(self) -> None:
        """Mute this string (stop ringing)."""
        self.muted = True
        self.ringing = False
        self.vibration_amp = 0.0

    def unmute(self) -> None:
        """Clear mute status."""
        self.muted = False

    def pluck(self) -> None:
        """Start ringing (clears mute flag)."""
        self.muted = False
        self.ringing = True
        self.vibration_amp = 1.0   # full amplitude; decays each frame

    def tick_animation(self, decay: float = 0.92) -> None:
        """
        Called once per frame. Reduces vibration amplitude by *decay*
        and clears ringing when amplitude falls below threshold.
        """
        self.vibration_amp *= decay
        if self.vibration_amp < 0.01:
            self.vibration_amp = 0.0
            self.ringing = False


@dataclass
class TouchTrace:
    """
    Tracks a single finger contact from touch-down to touch-up.

    Gesture recognition (GestureRecognizer) reads and updates this
    object as events arrive.
    """
    touch_id: int
    start_pos: Tuple[float, float]
    current_pos: Tuple[float, float]
    start_time: float                        # seconds since epoch
    current_time: float
    crossed_strings: List[int] = field(default_factory=list)  # string ids
    hold_active: bool = False

    @property
    def delta(self) -> Tuple[float, float]:
        """Displacement vector from start to current position."""
        return (
            self.current_pos[0] - self.start_pos[0],
            self.current_pos[1] - self.start_pos[1],
        )

    @property
    def distance(self) -> float:
        """Euclidean distance from start to current position."""
        dx, dy = self.delta
        return (dx * dx + dy * dy) ** 0.5

    @property
    def elapsed_ms(self) -> float:
        """Elapsed time since touch-down in milliseconds."""
        return (self.current_time - self.start_time) * 1000.0

    def update(self, pos: Tuple[float, float], t: float) -> None:
        """Update current position and timestamp."""
        self.current_pos = pos
        self.current_time = t

    """Tracks a single touch interaction across its lifetime."""

    touch_id: int
    start_pos: tuple[float, float] = (0.0, 0.0)
    current_pos: tuple[float, float] = (0.0, 0.0)
    start_time: float = 0.0
    current_time: float = 0.0
    crossed_strings: list[int] = field(default_factory=list)
    hold_active: bool = False

