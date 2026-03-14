from kivy.app import App
from kivy.core.window import Window
from kivy.graphics import Color, Line, Rectangle
from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.clock import Clock
from math import sin
import time


NOTES = [
    ("D2", 73.42),
    ("E2", 82.41),
    ("F2", 87.31),
    ("G2", 98.00),
    ("A2", 110.00),
    ("B2", 123.47),
    ("C3", 130.81),
    ("D3", 146.83),
]


class LyreString:
    def __init__(self, idx, note, freq, thickness):
        self.idx = idx
        self.note = note
        self.freq = freq
        self.thickness = thickness
        self.muted = False
        self.last_plucked = 0.0
        self.vibration = 0.0
        self.x = 0.0
        self.y1 = 0.0
        self.y2 = 0.0
        self.hitbox = 26


class LyreWidget(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        thicknesses = [4.5, 4.0, 3.6, 3.1, 2.7, 2.3, 2.0, 1.7]
        self.strings = [
            LyreString(i, note, freq, thicknesses[i])
            for i, (note, freq) in enumerate(NOTES)
        ]
        self.touch_state = {}
        Clock.schedule_interval(self.update_frame, 1 / 60)

    def on_size(self, *args):
        self.layout_strings()
        self.redraw()

    def on_pos(self, *args):
        self.layout_strings()
        self.redraw()

    def layout_strings(self):
        left = self.x + self.width * 0.25
        right = self.x + self.width * 0.75
        top = self.y + self.height * 0.82
        bottom = self.y + self.height * 0.18

        for i, s in enumerate(self.strings):
            t = i / (len(self.strings) - 1)
            s.x = left + (right - left) * t
            s.y1 = top
            s.y2 = bottom

    def redraw(self):
        self.canvas.clear()
        with self.canvas:
            Color(0.48, 0.31, 0.16)
            Rectangle(pos=(self.x + self.width * 0.22, self.y + self.height * 0.15),
                      size=(self.width * 0.56, self.height * 0.08))

            Color(0.57, 0.37, 0.18)
            Line(points=[
                self.x + self.width * 0.2, self.y + self.height * 0.2,
                self.x + self.width * 0.28, self.y + self.height * 0.82
            ], width=8)
            Line(points=[
                self.x + self.width * 0.8, self.y + self.height * 0.2,
                self.x + self.width * 0.72, self.y + self.height * 0.82
            ], width=8)
            Line(points=[
                self.x + self.width * 0.28, self.y + self.height * 0.82,
                self.x + self.width * 0.72, self.y + self.height * 0.82
            ], width=6)

            for s in self.strings:
                age = time.time() - s.last_plucked
                amp = max(0.0, s.vibration * (1.0 - age * 2.2))
                offset = sin(age * 32) * amp if amp > 0 else 0
                if s.muted:
                    Color(0.55, 0.45, 0.35)
                else:
                    Color(0.92, 0.87, 0.78)
                Line(points=[s.x + offset, s.y1, s.x + offset, s.y2], width=s.thickness)

    def find_string(self, x, y):
        best = None
        best_dist = 999999
        for s in self.strings:
            if s.y2 <= y <= s.y1:
                dist = abs(x - s.x)
                if dist < s.hitbox and dist < best_dist:
                    best = s
                    best_dist = dist
        return best

    def pluck_string(self, s, velocity=1.0):
        if s.muted:
            return
        s.last_plucked = time.time()
        s.vibration = max(6.0, min(18.0, 8.0 * velocity))
        print(f"PLUCK {s.note} {s.freq} Hz")

    def mute_string(self, s):
        s.muted = True
        s.vibration = 1.0

    def unmute_string(self, s):
        s.muted = False

    def on_touch_down(self, touch):
        if not self.collide_point(*touch.pos):
            return super().on_touch_down(touch)

        s = self.find_string(*touch.pos)
        self.touch_state[touch.uid] = {
            "start": touch.pos,
            "last": touch.pos,
            "time": time.time(),
            "crossed": set(),
            "string": s,
            "hold_active": False,
        }

        if s:
            self.pluck_string(s, velocity=1.0)
            self.touch_state[touch.uid]["crossed"].add(s.idx)
            return True

        return super().on_touch_down(touch)

    def on_touch_move(self, touch):
        state = self.touch_state.get(touch.uid)
        if not state:
            return super().on_touch_move(touch)

        px, py = state["last"]
        cx, cy = touch.pos

        for s in self.strings:
            crossed = ((px <= s.x <= cx) or (cx <= s.x <= px)) and (min(py, cy) <= s.y1 and max(py, cy) >= s.y2 or s.y2 <= cy <= s.y1)
            if crossed and s.idx not in state["crossed"]:
                self.pluck_string(s, velocity=max(0.6, min(2.0, abs(cx - px) / 35.0)))
                state["crossed"].add(s.idx)

        held_time = time.time() - state["time"]
        s = self.find_string(*touch.pos)
        if s and held_time > 0.15:
            self.mute_string(s)
            state["hold_active"] = True
            state["string"] = s

        state["last"] = touch.pos
        return True

    def on_touch_up(self, touch):
        state = self.touch_state.pop(touch.uid, None)
        if state and state["hold_active"] and state["string"]:
            self.unmute_string(state["string"])
            return True
        return super().on_touch_up(touch)

    def update_frame(self, dt):
        self.redraw()


class Root(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(orientation="vertical", **kwargs)
        self.add_widget(Label(
            text="Davidic Lyre  |  D Dorian  |  Swipe = Strum  |  Hold = Mute",
            size_hint=(1, 0.1)
        ))
        self.add_widget(LyreWidget(size_hint=(1, 0.9)))


class DavidicLyreApp(App):
    def build(self):
        Window.clearcolor = (0.92, 0.88, 0.80, 1)
        return Root()


if __name__ == "__main__":
    DavidicLyreApp().run()