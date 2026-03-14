"""
main.py — Entry point for the Davidic Lyre Android app.

Initializes the Kivy application, loads the main instrument screen,
and sets up the audio engine.
"""

from kivy.app import App

# TODO: Import main screen once app/screens.py is implemented
# from app.screens import MainScreen

# TODO: Import audio engine once app/audio_engine.py is implemented
# from app.audio_engine import AudioEngine


class DavidicLyreApp(App):
    """Main Kivy application class for the Davidic Lyre instrument app."""

    def build(self):
        """Build and return the root widget for the application."""
        # TODO: Initialize the audio engine
        # self.audio_engine = AudioEngine()
        # self.audio_engine.load_samples()

        # TODO: Load and return the main instrument screen
        # return MainScreen(audio_engine=self.audio_engine)

        # Placeholder root widget until screens are implemented
        from kivy.uix.label import Label
        return Label(text="Davidic Lyre — Coming Soon")

    def on_stop(self):
        """Clean up resources when the app is closed."""
        # TODO: Stop audio engine and release resources
        pass


if __name__ == "__main__":
    DavidicLyreApp().run()
