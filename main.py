"""
main.py – Entry point for the Davidic Lyre Android application.

Starts the Kivy app, initialises the audio engine, and creates the
main screen.  WAV samples are generated on first run if they are missing
from the assets/audio directory.
"""

import os
import sys

# ---------------------------------------------------------------------------
# Kivy environment must be configured before any kivy imports.
# ---------------------------------------------------------------------------
os.environ.setdefault("KIVY_NO_ENV_CONFIG", "1")

from kivy.app import App  # type: ignore  # noqa: E402
from kivy.uix.screenmanager import ScreenManager  # type: ignore  # noqa: E402

from app.audio_engine import AudioEngine, generate_wav_sample  # noqa: E402
from app.config import APP_TITLE  # noqa: E402
from app.screens import MainScreen  # noqa: E402
from app.tuning import ALL_PRESETS  # noqa: E402


# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
BASE_DIR   = os.path.dirname(os.path.abspath(__file__))
AUDIO_DIR  = os.path.join(BASE_DIR, "assets", "audio")
IMAGES_DIR = os.path.join(BASE_DIR, "assets", "images")


def _ensure_samples() -> None:
    """
    Generate any missing WAV sample files for all built-in presets.
    Uses only Python stdlib (wave + math) so no external dependencies are
    required on Android.
    """
    os.makedirs(AUDIO_DIR, exist_ok=True)
    seen: set[str] = set()

    for preset in ALL_PRESETS:
        for note, freq in zip(preset.notes, preset.frequencies):
            filename = f"lyre_{note.replace('#', 's')}.wav"
            if filename in seen:
                continue
            seen.add(filename)
            filepath = os.path.join(AUDIO_DIR, filename)
            if not os.path.isfile(filepath):
                print(f"[Davidic Lyre] Generating sample: {filename}")
                generate_wav_sample(freq, filepath)


class DavidicLyreApp(App):
    """Main Kivy application class."""

    title = APP_TITLE

    def build(self):
        _ensure_samples()

        self._audio = AudioEngine()
        from app.tuning import DEFAULT_PRESET
        self._audio.load_preset(DEFAULT_PRESET, AUDIO_DIR)

        sm = ScreenManager()
        sm.add_widget(
            MainScreen(
                audio_engine=self._audio,
                audio_dir=AUDIO_DIR,
                name="main",
            )
        )
        return sm

    def on_stop(self):
        self._audio.mute_all()


if __name__ == "__main__":
    DavidicLyreApp().run()
