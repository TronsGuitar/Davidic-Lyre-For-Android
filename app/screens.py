"""
app/screens.py – Screen definitions for the Davidic Lyre application.

MainScreen composes:
  - A top bar showing the app title and current preset name
  - The central LyreWidget
  - The ControlStrip at the bottom

SettingsPopup is a lightweight modal for extended options (future use).
"""

from kivy.graphics import Color, Rectangle  # type: ignore
from kivy.uix.boxlayout import BoxLayout  # type: ignore
from kivy.uix.label import Label  # type: ignore
from kivy.uix.modalview import ModalView  # type: ignore
from kivy.uix.screenmanager import Screen  # type: ignore

from app.audio_engine import AudioEngine
from app.config import (
    APP_TITLE,
    BOTTOM_BAR_H,
    COLORS,
    DEFAULT_DRONE_ON,
    HOLD_THRESHOLD_MS,
    TOP_BAR_H,
)
from app.controls import ControlStrip
from app.lyre_widget import LyreWidget
from app.tuning import get_preset_by_name


class MainScreen(Screen):
    """
    Primary instrument screen.

    Layout (portrait)::

        ┌─────────────────────────┐
        │   top bar (title)       │  TOP_BAR_H px
        ├─────────────────────────┤
        │                         │
        │      LyreWidget         │  flex
        │                         │
        ├─────────────────────────┤
        │   ControlStrip          │  BOTTOM_BAR_H px
        └─────────────────────────┘
    """

    def __init__(self, audio_engine: AudioEngine, audio_dir: str, **kwargs):
        super().__init__(**kwargs)
        self._audio_engine = audio_engine
        self._audio_dir    = audio_dir
        self._drone_on     = DEFAULT_DRONE_ON
        self._title_label: Label | None = None

        self._build()

    def _build(self) -> None:
        root = BoxLayout(orientation="vertical")

        # --- top bar ---
        top_bar = BoxLayout(
            orientation="horizontal",
            size_hint_y=None,
            height=TOP_BAR_H,
        )
        with top_bar.canvas.before:
            Color(*COLORS["dark_wood"])
            self._top_rect = Rectangle(size=top_bar.size, pos=top_bar.pos)
        top_bar.bind(
            size=lambda w, v: setattr(self._top_rect, "size", v),
            pos=lambda w, v: setattr(self._top_rect, "pos", v),
        )
        self._title_label = Label(
            text=APP_TITLE,
            font_size="20sp",
            color=COLORS["label_text"],
            bold=True,
        )
        top_bar.add_widget(self._title_label)

        # --- lyre widget ---
        self._lyre = LyreWidget(
            audio_engine=self._audio_engine,
            size_hint=(1, 1),
        )

        # --- control strip ---
        self._controls = ControlStrip()
        self._controls.on_preset_change = self._on_preset_change
        self._controls.on_labels_toggle = self._lyre.set_labels
        self._controls.on_drone_toggle  = self._on_drone_toggle
        self._controls.on_tone_toggle   = self._on_tone_toggle
        self._controls.on_mute_sens     = self._on_mute_sens
        self._controls.on_reverb        = self._on_reverb_change
        self._controls.on_left_hand     = self._lyre.set_left_hand

        root.add_widget(top_bar)
        root.add_widget(self._lyre)
        root.add_widget(self._controls)
        self.add_widget(root)

    # ------------------------------------------------------------------
    # Kivy lifecycle
    # ------------------------------------------------------------------

    def on_enter(self, *args) -> None:
        """Load the default preset when the screen becomes active."""
        from app.tuning import DEFAULT_PRESET
        self._load_preset(DEFAULT_PRESET.name)

    # ------------------------------------------------------------------
    # Control callbacks
    # ------------------------------------------------------------------

    def _on_preset_change(self, name: str) -> None:
        self._load_preset(name)

    def _load_preset(self, name: str) -> None:
        preset = get_preset_by_name(name)
        self._audio_engine.load_preset(preset, self._audio_dir)
        self._lyre.load_preset(preset)
        if self._title_label:
            self._title_label.text = f"{APP_TITLE}  –  {preset.name}"

    def _on_drone_toggle(self, active: bool) -> None:
        self._drone_on = active
        if active:
            # Pluck string 0 at full gain as a sustained drone anchor
            self._audio_engine.pluck(0, 1.0)
        else:
            self._audio_engine.mute(0)

    def _on_tone_toggle(self, ancient: bool) -> None:
        # In the MVP this is a placeholder.  A future version will switch
        # between a richer (ancient) impulse response and a clean signal.
        pass

    def _on_mute_sens(self, value: float) -> None:
        """
        Map slider value (0–1) to a hold-threshold multiplier.
        value=0 → 50 ms (very sensitive), value=1 → 400 ms (insensitive).
        """
        ms = 50 + value * 350
        self._lyre._gesture.hold_threshold_ms = ms

    def _on_reverb_change(self, value: float) -> None:
        self._audio_engine.reverb_amount = value


# ---------------------------------------------------------------------------
# Settings popup (placeholder – for future settings that don't fit the strip)
# ---------------------------------------------------------------------------

class SettingsPopup(ModalView):
    """
    A modal overlay for extended settings.  Placeholder in MVP.
    """

    def __init__(self, **kwargs):
        kwargs.setdefault("size_hint", (0.85, 0.6))
        super().__init__(**kwargs)
        layout = BoxLayout(orientation="vertical", padding=16, spacing=8)
        layout.add_widget(Label(
            text="Extended Settings\n(coming in v2)",
            halign="center",
        ))
        self.add_widget(layout)
