
"""
app/controls.py – Bottom control strip for the Davidic Lyre.

Provides:
  - Tuning preset dropdown
  - Labels on/off toggle
  - Drone on/off toggle
  - Tone selector (ancient / clean)
  - Mute sensitivity slider
  - Reverb amount slider
  - Left-handed mode toggle

All UI state changes are forwarded to callbacks set by the parent screen.
"""

from typing import Callable, Optional

from kivy.uix.boxlayout import BoxLayout  # type: ignore
from kivy.uix.button import Button  # type: ignore
from kivy.uix.label import Label  # type: ignore
from kivy.uix.slider import Slider  # type: ignore
from kivy.uix.spinner import Spinner  # type: ignore
from kivy.uix.togglebutton import ToggleButton  # type: ignore

from app.config import (
    BOTTOM_BAR_H,
    DEFAULT_DRONE_ON,
    DEFAULT_LABELS_ON,
    DEFAULT_LEFT_HAND,
    DEFAULT_MUTE_SENS,
    DEFAULT_REVERB,
)
from app.tuning import ALL_PRESETS, DEFAULT_PRESET


class ControlStrip(BoxLayout):
    """
    A horizontal strip of controls shown at the bottom of the main screen.
    """

    def __init__(self, **kwargs):
        kwargs.setdefault("orientation", "horizontal")
        kwargs.setdefault("size_hint_y", None)
        kwargs.setdefault("height", BOTTOM_BAR_H)
        kwargs.setdefault("spacing", 6)
        kwargs.setdefault("padding", [8, 4, 8, 4])
        super().__init__(**kwargs)

        # Callbacks (set by parent)
        self.on_preset_change: Optional[Callable] = None
        self.on_labels_toggle: Optional[Callable] = None
        self.on_drone_toggle:  Optional[Callable] = None
        self.on_tone_toggle:   Optional[Callable] = None
        self.on_mute_sens:     Optional[Callable] = None
        self.on_reverb:        Optional[Callable] = None
        self.on_left_hand:     Optional[Callable] = None

        self._build()

    def _build(self) -> None:
        # --- Tuning preset dropdown ---
        preset_names = [p.name for p in ALL_PRESETS]
        self._spinner = Spinner(
            text=DEFAULT_PRESET.name,
            values=preset_names,
            size_hint_x=0.30,
            font_size="13sp",
        )
        self._spinner.bind(text=self._preset_changed)
        self.add_widget(self._spinner)

        # --- Labels toggle ---
        self._lbl_btn = ToggleButton(
            text="Labels",
            size_hint_x=0.12,
            state="down" if DEFAULT_LABELS_ON else "normal",
            font_size="12sp",
        )
        self._lbl_btn.bind(on_press=self._labels_toggled)
        self.add_widget(self._lbl_btn)

        # --- Drone toggle ---
        self._drone_btn = ToggleButton(
            text="Drone",
            size_hint_x=0.12,
            state="down" if DEFAULT_DRONE_ON else "normal",
            font_size="12sp",
        )
        self._drone_btn.bind(on_press=self._drone_toggled)
        self.add_widget(self._drone_btn)

        # --- Tone toggle (ancient / clean) ---
        self._tone_btn = ToggleButton(
            text="Ancient",
            size_hint_x=0.12,
            state="down",
            font_size="12sp",
        )
        self._tone_btn.bind(on_press=self._tone_toggled)
        self.add_widget(self._tone_btn)

        # --- Mute sensitivity slider ---
        self.add_widget(Label(
            text="Mute",
            size_hint_x=0.06,
            font_size="11sp",
        ))
        self._mute_slider = Slider(
            min=0.0,
            max=1.0,
            value=DEFAULT_MUTE_SENS,
            size_hint_x=0.10,
        )
        self._mute_slider.bind(value=self._mute_sens_changed)
        self.add_widget(self._mute_slider)

        # --- Reverb slider ---
        self.add_widget(Label(
            text="Reverb",
            size_hint_x=0.07,
            font_size="11sp",
        ))
        self._reverb_slider = Slider(
            min=0.0,
            max=1.0,
            value=DEFAULT_REVERB,
            size_hint_x=0.10,
        )
        self._reverb_slider.bind(value=self._reverb_changed)
        self.add_widget(self._reverb_slider)

        # --- Left-handed toggle ---
        self._lh_btn = ToggleButton(
            text="↔",
            size_hint_x=0.08,
            state="down" if DEFAULT_LEFT_HAND else "normal",
            font_size="14sp",
        )
        self._lh_btn.bind(on_press=self._left_hand_toggled)
        self.add_widget(self._lh_btn)

    # ------------------------------------------------------------------
    # Event handlers
    # ------------------------------------------------------------------

    def _preset_changed(self, spinner, text: str) -> None:
        if self.on_preset_change:
            self.on_preset_change(text)

    def _labels_toggled(self, btn) -> None:
        if self.on_labels_toggle:
            self.on_labels_toggle(btn.state == "down")

    def _drone_toggled(self, btn) -> None:
        if self.on_drone_toggle:
            self.on_drone_toggle(btn.state == "down")

    def _tone_toggled(self, btn) -> None:
        if self.on_tone_toggle:
            self.on_tone_toggle(btn.state == "down")

    def _mute_sens_changed(self, slider, value: float) -> None:
        if self.on_mute_sens:
            self.on_mute_sens(value)

    def _reverb_changed(self, slider, value: float) -> None:
        if self.on_reverb:
            self.on_reverb(value)

    def _left_hand_toggled(self, btn) -> None:
        if self.on_left_hand:
            self.on_left_hand(btn.state == "down")