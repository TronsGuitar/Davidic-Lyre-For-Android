# Davidic Lyre for Android
A Python mobile instrument app that simulates an ancient David-style lyre on a Samsung Galaxy Fold5 using Kivy.

## 1. Product Summary

Build a touch-based digital lyre inspired by reconstructions of the ancient Hebrew kinnor. The app should look like a small wooden gut-string lyre and sound warm, dry, and organic. The user interacts through direct touch:

- tap to pluck a string
- swipe across strings to strum
- hold on a string to mute it
- drag while holding to mute multiple strings
- optional drone mode for psalm-style accompaniment

The app must run well on the Fold5 inner screen in portrait mode and remain usable on the outer screen.

---

## 2. Goals

### Primary goals
- Simulate an 8-string David-style lyre
- Deliver responsive multi-touch performance
- Recreate a gut-string, wooden-body sound
- Support swipe strumming and hold muting
- Provide historically inspired tuning presets
- Run on Android using Python

### Secondary goals
- Visual string vibration
- Left-handed mode
- Manual retuning
- Recording and export
- Practice mode for psalm melodies

---

## 3. Non-Goals for MVP

Do not include these in v1:
- advanced physical modeling synthesis
- network features
- user accounts
- cloud sync
- MIDI support
- notation editor
- full DAW features

---

## 4. User Stories

### Core user stories
- As a user, I want to tap a string and hear it pluck instantly.
- As a user, I want to swipe across strings and hear a natural strum in the order I crossed them.
- As a user, I want to hold a string to mute it and stop its ringing.
- As a user, I want the lyre to sound warm and ancient rather than metallic.
- As a user, I want to play a D Dorian psalm drone without setup.
- As a user, I want the instrument to scale well on my Fold5 screen.

### Stretch user stories
- As a user, I want to retune strings to alternate ancient modes.
- As a user, I want a drone lock on the lowest string.
- As a user, I want a left-handed layout option.
- As a user, I want to record short performances.

---

## 5. Platform and Technical Stack

### Target platform
- Android
- Samsung Galaxy Fold5
- Portrait unfolded mode is primary

### Language and framework
- Python 3.11 or compatible version supported by Buildozer
- Kivy for UI, canvas drawing, input, animation
- Buildozer for Android packaging

### Audio
- Sample-based playback for MVP
- Preloaded WAV samples
- Per-string envelope shaping
- Optional body resonance layer

---

## 6. Instrument Specification

### Historical inspiration
The app should visually resemble a reconstructed ancient Near Eastern lyre:
- rounded lower resonator
- two upright arms
- top crossbar
- 8 strings
- natural wood textures
- cream-to-amber gut strings
- thicker low strings, thinner high strings

### Visual tone
- warm brown woods
- slight handmade asymmetry
- simple ancient aesthetic
- no steel machine tuners
- visible wrapped string knots or loops at the crossbar

### Suggested color palette
- light wood: #A87442
- medium wood: #7A4E2A
- dark wood: #4A2E1A
- highlight wear: #C99562
- gut string light: #E8DCC8
- gut string dark: #9A6E45

---

## 7. Tuning Specification

### Default tuning preset
Davidic D Dorian:
- D2 = 73.42 Hz
- E2 = 82.41 Hz
- F2 = 87.31 Hz
- G2 = 98.00 Hz
- A2 = 110.00 Hz
- B2 = 123.47 Hz
- C3 = 130.81 Hz
- D3 = 146.83 Hz

### Alternate dark preset
Davidic dark mode:
- D2
- E2
- F2
- G2
- A2
- Bb2
- C3
- D3

### Optional drone preset
Drone psalm:
- D2
- A2
- D3
- F3
- G3
- A3
- C4
- D4

---

## 8. Interaction Specification

### Tap
- Touch directly on a string hitbox
- Trigger one pluck event
- Volume based on tap speed proxy if available
- Immediate retrigger allowed

### Swipe strum
- A moving finger crossing string hitboxes triggers each crossed string
- Strings play in crossing order
- Swipe speed controls velocity
- Direction must match on-screen order
- Full strum must sound sequential, not chord-stacked at once

### Hold mute
- A touch held on a string beyond threshold activates mute
- Mute threshold: 150 ms default
- Muted strings stop or strongly damp current ringing
- Muted strings cannot ring normally while held

### Drag mute
- While holding, dragging across adjacent strings mutes them as they are crossed

### Drone mode
- Optional toggle
- Lowest string or selected string sustains more strongly
- User can latch drone with hold or double-tap, depending on setting

---

## 9. Audio Behavior

### Sound character
- warm
- short to medium sustain
- low metallic content
- mild pitch drift
- woody resonance
- soft initial attack

### Sample approach
Each string uses one sample or a pitch-shifted base sample.
Preferred file format:
- WAV
- mono
- 44.1 kHz or 48 kHz
- dry recording
- no baked reverb

### Envelope
Suggested ADSR:
- Attack: 0.005 to 0.015 s
- Decay: 0.12 to 0.25 s
- Sustain: 0.25 to 0.45
- Release: 0.20 to 0.80 s

### Sympathetic resonance, optional
- Related strings receive low-level resonance
- Max 15 percent of source amplitude
- Keep subtle

---

## 10. Visual Animation

### String vibration
- On pluck, string visually oscillates side to side
- Oscillation amplitude depends on pluck velocity
- Animation decays with envelope

### Mute visual
- Muted string darkens slightly
- Vibration drops quickly
- Optional muted indicator dot near touch point

### Active note labels
Optional overlay:
- note name
- frequency in Hz

---

## 11. Accessibility and Layout

### Main layout
Portrait unfolded mode:
- top bar for title and tuning
- center large lyre widget
- bottom control strip

### Controls
- Tuning preset dropdown
- Labels on/off
- Drone on/off
- Ancient or clean tone
- Mute sensitivity
- Reverb amount
- Left-handed mode

### Accessibility
- expanded invisible hitboxes for strings
- high-contrast mode
- optional vibration feedback
- scalable UI for outer screen

---

## 12. Performance Requirements

### Audio latency
- target under 30 ms
- ideal under 20 ms

### Frame rate
- target 60 FPS on main screen

### Polyphony
- minimum 8 simultaneous voices
- recommended 16 or more to allow resonance tails

### Memory
- keep total audio assets under 50 MB for MVP
- app footprint under 200 MB preferred

---

## 13. Architecture

### Directory structure
.
├── PROD.md
├── README.md
├── requirements.txt
├── buildozer.spec
├── main.py
├── assets
│   ├── audio
│   │   ├── lyre_D2.wav
│   │   ├── lyre_E2.wav
│   │   ├── lyre_F2.wav
│   │   ├── lyre_G2.wav
│   │   ├── lyre_A2.wav
│   │   ├── lyre_B2.wav
│   │   ├── lyre_C3.wav
│   │   └── lyre_D3.wav
│   └── images
│       └── wood_texture.png
├── app
│   ├── __init__.py
│   ├── config.py
│   ├── tuning.py
│   ├── models.py
│   ├── gestures.py
│   ├── audio_engine.py
│   ├── lyre_widget.py
│   ├── controls.py
│   └── screens.py
└── tests
    ├── test_tuning.py
    ├── test_gestures.py
    └── test_string_model.py

---

## 14. Module Responsibilities

### main.py
- starts Kivy app
- loads main screen
- initializes audio engine

### app/config.py
- constants
- UI dimensions
- thresholds
- default presets

### app/tuning.py
- note names
- frequency maps
- preset definitions

### app/models.py
- LyreString class
- TouchTrace class
- TuningPreset class

### app/gestures.py
- swipe detection
- hold threshold tracking
- segment and hitbox crossing detection

### app/audio_engine.py
- sample load
- playback control
- mute logic
- envelopes
- polyphony management

### app/lyre_widget.py
- instrument drawing
- touch event routing
- string animations
- note labels

### app/controls.py
- toggles
- dropdowns
- sliders

### app/screens.py
- main instrument screen
- settings popups
- optional recording screen

---

## 15. Data Models

### LyreString
Fields:
- id: int
- note_name: str
- frequency: float
- x: float
- y_top: float
- y_bottom: float
- thickness_px: float
- hitbox_width_px: float
- muted: bool
- ringing: bool
- gain: float
- sample_path: str

### TouchTrace
Fields:
- touch_id: int
- start_pos: tuple[float, float]
- current_pos: tuple[float, float]
- start_time: float
- current_time: float
- crossed_strings: list[int]
- hold_active: bool

### TuningPreset
Fields:
- name: str
- notes: list[str]
- frequencies: list[float]

---

## 16. Gesture Algorithms

### Tap detection
- Identify nearest string hitbox on touch down
- If movement stays below tap distance threshold and release occurs before hold threshold, pluck

### Hold detection
- On touch down over a string, start timer
- If touch remains within hold radius for threshold duration, activate mute for that string

### Swipe detection
- On touch move, compare previous and current positions
- Detect all string hitboxes crossed by the segment
- Order by crossing position along movement vector
- Trigger pluck events in that sequence

### Threshold defaults
- tap drift tolerance: 18 px
- hold drift tolerance: 22 px
- hold threshold: 150 ms
- minimum swipe distance: 25 px

---

## 17. Acceptance Criteria

### MVP accepted when
- app runs on Fold5
- tap pluck works on all 8 strings
- swipe strum works both directions
- hold mute works reliably
- strings visibly vibrate
- D Dorian preset loads by default
- tone feels woody and non-metallic
- UI remains responsive under multi-touch

---

## 18. Future Enhancements

### V2
- manual retuning
- recording and export
- drone latch
- alternate lyre body shapes
- historical presets
- practice mode with guided psalm phrases

### V3
- physical modeling hybrid
- MIDI out
- external audio support
- layered temple ambience
