"""UI controls: tuning preset dropdown, labels toggle, drone toggle."""

from __future__ import annotations

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.dropdown import DropDown
from kivy.uix.label import Label

from app.tuning import ALL_PRESETS, DEFAULT_PRESET, TuningPreset


class TuningDropdown(BoxLayout):
    """A dropdown selector for tuning presets."""

    def __init__(self, on_select_callback=None, **kwargs):
        super().__init__(size_hint=(None, None), size=(200, 44), **kwargs)
        self._callback = on_select_callback
        self._current = DEFAULT_PRESET

        self._button = Button(text=self._current.name, size_hint=(1, 1))
        self._button.bind(on_release=self._open_dropdown)
        self.add_widget(self._button)

        self._dropdown = DropDown()
        for preset in ALL_PRESETS:
            btn = Button(text=preset.name, size_hint_y=None, height=44)
            btn.bind(on_release=lambda btn, p=preset: self._select(p))
            self._dropdown.add_widget(btn)

    def _open_dropdown(self, widget):
        self._dropdown.open(widget)

    def _select(self, preset: TuningPreset):
        self._dropdown.dismiss()
        self._current = preset
        self._button.text = preset.name
        if self._callback:
            self._callback(preset)

    @property
    def current_preset(self) -> TuningPreset:
        return self._current


class HeaderBar(BoxLayout):
    """Top bar with title and tuning selector."""

    def __init__(self, on_preset_change=None, **kwargs):
        super().__init__(size_hint=(1, None), height=48, **kwargs)
        self.add_widget(Label(text="Davidic Lyre", size_hint=(0.5, 1)))
        self.tuning = TuningDropdown(on_select_callback=on_preset_change)
        self.add_widget(self.tuning)
