"""Davidic Lyre for Android — entry point.

Starts the Kivy application, initialises the audio engine and loads the
default D Dorian tuning preset.
"""

from kivy.app import App
from kivy.core.window import Window

from app.config import COLOR_BACKGROUND
from app.screens import MainScreen


class DavidicLyreApp(App):
    """Root Kivy application."""

    def build(self):
        Window.clearcolor = COLOR_BACKGROUND
        return MainScreen()


if __name__ == "__main__":
    DavidicLyreApp().run()
