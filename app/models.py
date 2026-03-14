"""Data model classes for the Davidic Lyre."""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class TuningPreset:
    """A named tuning configuration for the lyre's eight strings."""

    name: str
    notes: list[str]
    frequencies: list[float]

    def __post_init__(self) -> None:
        if len(self.notes) != len(self.frequencies):
            raise ValueError("notes and frequencies must have the same length")


@dataclass
class LyreString:
    """State for a single lyre string."""

    idx: int
    note: str
    frequency: float
    thickness: float
    x: float = 0.0
    y_top: float = 0.0
    y_bottom: float = 0.0
    hitbox_width: float = 26.0
    muted: bool = False
    ringing: bool = False
    gain: float = 1.0
    last_plucked: float = 0.0
    vibration: float = 0.0
    sample_path: str = ""

    @property
    def note_name(self) -> str:
        return self.note


@dataclass
class TouchTrace:
    """Tracks a single touch interaction across its lifetime."""

    touch_id: int
    start_pos: tuple[float, float] = (0.0, 0.0)
    current_pos: tuple[float, float] = (0.0, 0.0)
    start_time: float = 0.0
    current_time: float = 0.0
    crossed_strings: list[int] = field(default_factory=list)
    hold_active: bool = False
