"""
app/controls.py — UI toggles, dropdowns, and sliders for the Davidic Lyre app.

Provides the control strip at the bottom of the main screen (PRD Section 11),
including:
  - Tuning preset dropdown
  - Note-labels on/off toggle
  - Drone mode on/off toggle
  - Tone selector (Ancient / Clean)
  - Mute sensitivity slider
  - Reverb amount slider
  - Left-handed mode toggle

All controls communicate with the :class:`~app.lyre_widget.LyreWidget` and
:class:`~app.audio_engine.AudioEngine` through callback props or an event bus
that will be wired up in Phase 1.
"""

# TODO: Import Kivy layout and widget classes in Phase 1
# from kivy.uix.boxlayout import BoxLayout
# from kivy.uix.spinner import Spinner
# from kivy.uix.togglebutton import ToggleButton
# from kivy.uix.slider import Slider

from app.tuning import ALL_PRESETS


class ControlStrip:
    """Bottom control strip providing tuning and playback options.

    In Phase 1 this class will extend a Kivy layout widget.  For now it is a
    plain Python stub to satisfy imports and allow unit testing of logic.
    """

    def __init__(self) -> None:
        # TODO: Build Kivy widget tree in Phase 1
        self.preset_names = [p["name"] for p in ALL_PRESETS]
        self.current_preset_name: str = self.preset_names[0]
        self.labels_visible: bool = False
        self.drone_active: bool = False
        self.tone_ancient: bool = True
        self.mute_sensitivity: float = 1.0   # 0.0–1.0 maps to threshold scaling
        self.reverb_amount: float = 0.0       # 0.0–1.0
        self.left_handed: bool = False

    # ------------------------------------------------------------------
    # Preset selector
    # ------------------------------------------------------------------

    def _on_preset_change(self, preset_name: str) -> None:
        """Called when the user selects a different tuning preset.

        Args:
            preset_name: The human-readable name of the selected preset.
        """
        # TODO: Look up preset, notify LyreWidget to rebuild string layout (Phase 1)
        self.current_preset_name = preset_name
        raise NotImplementedError("Preset change handler not yet implemented")

    # ------------------------------------------------------------------
    # Toggles
    # ------------------------------------------------------------------

    def _on_labels_toggle(self, active: bool) -> None:
        """Toggle note-name label overlay on the lyre widget."""
        # TODO: Set LyreWidget.labels_visible (Phase 1)
        self.labels_visible = active
        raise NotImplementedError("Labels toggle not yet implemented")

    def _on_drone_toggle(self, active: bool) -> None:
        """Toggle drone mode on the audio engine."""
        # TODO: Notify AudioEngine of drone state change (Phase 1)
        self.drone_active = active
        raise NotImplementedError("Drone toggle not yet implemented")

    def _on_tone_toggle(self, ancient: bool) -> None:
        """Switch between Ancient and Clean tone profiles."""
        # TODO: Apply tone preset to AudioEngine (Phase 1)
        self.tone_ancient = ancient
        raise NotImplementedError("Tone toggle not yet implemented")

    # ------------------------------------------------------------------
    # Sliders
    # ------------------------------------------------------------------

    def _on_mute_sensitivity_change(self, value: float) -> None:
        """Update the mute-sensitivity (hold threshold) scaling factor.

        Args:
            value: Slider value in the range 0.0–1.0.
        """
        # TODO: Map value to MUTE_THRESHOLD_MS scaling and update config (Phase 1)
        self.mute_sensitivity = value
        raise NotImplementedError("Mute sensitivity slider not yet implemented")

    def _on_reverb_change(self, value: float) -> None:
        """Update the reverb send level on the audio engine.

        Args:
            value: Slider value in the range 0.0–1.0.
        """
        # TODO: Pass value to AudioEngine reverb bus (Phase 1)
        self.reverb_amount = value
        raise NotImplementedError("Reverb slider not yet implemented")

    # ------------------------------------------------------------------
    # Layout
    # ------------------------------------------------------------------

    def _on_left_handed_toggle(self, active: bool) -> None:
        """Mirror the lyre widget for left-handed players."""
        # TODO: Instruct LyreWidget to flip its string layout (Phase 1)
        self.left_handed = active
        raise NotImplementedError("Left-handed toggle not yet implemented")
