"""
app/lyre_widget.py — Instrument drawing on the Kivy canvas, touch event routing,
string animations, and note-name label overlays.

Renders the 8-string lyre instrument and handles all Kivy touch input, delegating
gesture classification to :mod:`app.gestures` and audio output to
:mod:`app.audio_engine`.  Visual style follows the colour palette and layout
guidelines in PRD Sections 6 and 11.

Responsibilities:
  - Draw the lyre body (resonator, arms, crossbar) using Kivy canvas instructions
  - Draw and animate 8 strings with thickness proportional to pitch
  - Route touch events through the gesture recogniser
  - Trigger pluck / mute callbacks on the audio engine
  - Optionally render note-name / frequency label overlays
"""

# TODO: Import Kivy widget classes in Phase 1
# from kivy.uix.widget import Widget
# from kivy.graphics import Line, Color, Ellipse
# from kivy.clock import Clock

from app.audio_engine import AudioEngine
from app.gestures import find_crossed_strings, is_tap, check_hold
from app.models import LyreString, TouchTrace, TuningPreset


class LyreWidget:
    """Kivy Widget that renders the lyre and handles touch interactions.

    In Phase 1 this class will extend ``kivy.uix.widget.Widget``.  For now
    it is a plain Python stub so the module can be imported without a running
    Kivy environment.
    """

    def __init__(self, audio_engine: AudioEngine, preset: TuningPreset) -> None:
        # TODO: Call super().__init__() once Widget base is added (Phase 1)
        self.audio_engine = audio_engine
        self.preset = preset
        self.strings: list = []  # List[LyreString]
        self.active_traces: dict = {}  # touch_id -> TouchTrace

        # TODO: Build LyreString list from preset and widget dimensions (Phase 1)
        # TODO: Bind widget size/pos to _rebuild_layout (Phase 1)

    # ------------------------------------------------------------------
    # Layout
    # ------------------------------------------------------------------

    def _rebuild_layout(self, *args) -> None:
        """Recompute string positions and hitboxes after a resize."""
        # TODO: Distribute strings evenly across widget width,
        #       scale y_top/y_bottom to widget height (Phase 1)
        raise NotImplementedError("Layout not yet implemented")

    # ------------------------------------------------------------------
    # Drawing
    # ------------------------------------------------------------------

    def _draw_body(self) -> None:
        """Draw the lyre body (resonator, arms, crossbar) on the Kivy canvas."""
        # TODO: Use Kivy canvas instructions with PRD color palette (Phase 1)
        # Colors: COLOR_LIGHT_WOOD, COLOR_MEDIUM_WOOD, COLOR_DARK_WOOD
        raise NotImplementedError("Lyre body drawing not yet implemented")

    def _draw_strings(self) -> None:
        """Draw all 8 strings with thickness proportional to pitch."""
        # TODO: Iterate self.strings; lower-pitched strings are thicker (Phase 1)
        raise NotImplementedError("String drawing not yet implemented")

    def _draw_labels(self) -> None:
        """Draw optional note-name / frequency overlay labels."""
        # TODO: Render CoreLabel for each string when labels_visible is True (Phase 1)
        raise NotImplementedError("Label drawing not yet implemented")

    def _animate_string(self, string_id: int, velocity: float) -> None:
        """Start the side-oscillation animation for the plucked string.

        Args:
            string_id: ID of the string to animate.
            velocity: Pluck velocity (0.0–1.0) controlling oscillation amplitude.
        """
        # TODO: Schedule oscillation frames with Clock.schedule_interval (Phase 1)
        # PRD Section 10: oscillation amplitude scales with velocity,
        # decays in sync with ADSR envelope.
        raise NotImplementedError("String animation not yet implemented")

    # ------------------------------------------------------------------
    # Touch handling
    # ------------------------------------------------------------------

    def on_touch_down(self, touch) -> bool:
        """Handle a new finger contact."""
        # TODO: Create TouchTrace, detect nearest string, start hold timer (Phase 1)
        raise NotImplementedError("Touch-down handling not yet implemented")

    def on_touch_move(self, touch) -> bool:
        """Handle finger movement, detecting swipe crossings."""
        # TODO: Update TouchTrace, call find_crossed_strings, trigger plucks (Phase 1)
        raise NotImplementedError("Touch-move handling not yet implemented")

    def on_touch_up(self, touch) -> bool:
        """Handle finger lift, finalising tap or ending hold."""
        # TODO: Classify gesture with is_tap, clean up TouchTrace (Phase 1)
        raise NotImplementedError("Touch-up handling not yet implemented")
