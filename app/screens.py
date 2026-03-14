"""
app/screens.py — Main instrument screen, settings popups, and optional recording
screen for the Davidic Lyre app.

Composes the top-level Kivy screen hierarchy (PRD Section 11):
  - MainScreen   — title bar + LyreWidget + ControlStrip
  - SettingsPopup — modal overlay for advanced preferences
  - RecordingScreen (optional) — simple capture + export UI (Phase V2)

Screen transitions and ScreenManager registration will be wired up in Phase 1.
"""

# TODO: Import Kivy screen classes in Phase 1
# from kivy.uix.screenmanager import Screen, ScreenManager
# from kivy.uix.boxlayout import BoxLayout
# from kivy.uix.label import Label
# from kivy.uix.popup import Popup

from app.audio_engine import AudioEngine
from app.controls import ControlStrip
from app.lyre_widget import LyreWidget
from app.tuning import DEFAULT_PRESET


class MainScreen:
    """Primary instrument screen shown on app launch.

    Layout (portrait, PRD Section 11):
    - Top bar  : app title + active tuning preset name
    - Centre   : LyreWidget (occupies most of the screen height)
    - Bottom   : ControlStrip

    In Phase 1 this class will extend ``kivy.uix.screenmanager.Screen``.
    """

    def __init__(self, audio_engine: AudioEngine) -> None:
        # TODO: Call super().__init__(name="main") in Phase 1
        self.audio_engine = audio_engine

        # TODO: Instantiate and compose child widgets in Phase 1
        # self.lyre_widget = LyreWidget(audio_engine=audio_engine,
        #                               preset=DEFAULT_PRESET)
        # self.controls = ControlStrip()
        # Wire up controls -> lyre_widget -> audio_engine callbacks

    def on_enter(self) -> None:
        """Called by ScreenManager when this screen becomes active."""
        # TODO: Resume audio engine and refresh lyre layout (Phase 1)
        raise NotImplementedError("MainScreen.on_enter not yet implemented")

    def on_leave(self) -> None:
        """Called by ScreenManager when navigating away from this screen."""
        # TODO: Pause audio engine (Phase 1)
        raise NotImplementedError("MainScreen.on_leave not yet implemented")


class SettingsPopup:
    """Modal popup for settings not exposed in the main control strip.

    Future settings may include ADSR fine-tuning, sympathetic resonance
    level, and accessibility options.

    In Phase 1 this class will extend ``kivy.uix.popup.Popup``.
    """

    def __init__(self) -> None:
        # TODO: Build settings form widgets in Phase 1
        pass

    def open(self) -> None:
        """Display the settings popup over the current screen."""
        # TODO: Call super().open() in Phase 1
        raise NotImplementedError("SettingsPopup.open not yet implemented")

    def dismiss(self) -> None:
        """Close the settings popup."""
        # TODO: Call super().dismiss() in Phase 1
        raise NotImplementedError("SettingsPopup.dismiss not yet implemented")


class RecordingScreen:
    """Optional screen for recording and exporting short performances.

    Planned for Phase V2 (PRD Section 18).

    In Phase 1+ this class will extend ``kivy.uix.screenmanager.Screen``.
    """

    def __init__(self) -> None:
        # TODO: Implement recording UI (Phase V2)
        pass

    def start_recording(self) -> None:
        """Begin capturing audio output."""
        # TODO: Implement audio capture (Phase V2)
        raise NotImplementedError("RecordingScreen.start_recording not yet implemented")

    def stop_recording(self) -> None:
        """Stop capture and prompt user to save or share."""
        # TODO: Implement stop + export dialog (Phase V2)
        raise NotImplementedError("RecordingScreen.stop_recording not yet implemented")
