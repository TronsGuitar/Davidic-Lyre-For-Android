"""Screen management for the Davidic Lyre app."""

from __future__ import annotations

from kivy.uix.boxlayout import BoxLayout

from app.audio_engine import AudioEngine, ensure_samples
from app.controls import HeaderBar
from app.lyre_widget import LyreWidget
from app.tuning import DEFAULT_PRESET, TuningPreset


class MainScreen(BoxLayout):
    """Primary instrument screen containing the header and lyre widget."""

    def __init__(self, **kwargs):
        super().__init__(orientation="vertical", **kwargs)

        self.audio_engine = AudioEngine()
        self.lyre = LyreWidget(audio_engine=self.audio_engine)
        self.header = HeaderBar(on_preset_change=self._apply_preset)

        self.add_widget(self.header)
        self.add_widget(self.lyre)

        # Load default tuning
        self._apply_preset(DEFAULT_PRESET)

    def _apply_preset(self, preset: TuningPreset) -> None:
        """Apply a tuning preset: load samples and configure strings."""
        paths = ensure_samples(preset.notes, preset.frequencies)
        for note, path in paths.items():
            self.audio_engine.load(note, path)
        self.lyre.set_strings(preset.notes, preset.frequencies)
