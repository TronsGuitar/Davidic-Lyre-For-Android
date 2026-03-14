"""
app/config.py – Global constants, UI dimensions, thresholds, and colour palette
for the Davidic Lyre for Android application.
"""

# ---------------------------------------------------------------------------
# Colour palette (RGBA tuples, values 0.0–1.0)
# ---------------------------------------------------------------------------
COLORS = {
    "light_wood":     (0.659, 0.455, 0.259, 1.0),
    "medium_wood":    (0.478, 0.306, 0.165, 1.0),
    "dark_wood":      (0.290, 0.180, 0.102, 1.0),
    "highlight_wear": (0.788, 0.584, 0.384, 1.0),
    "gut_string_light": (0.910, 0.863, 0.784, 1.0),
    "gut_string_dark":  (0.604, 0.431, 0.271, 1.0),
    "muted_overlay":  (0.15, 0.08, 0.04, 0.45),
    "label_text":     (0.95, 0.90, 0.80, 1.0),
    "background":     (0.12, 0.07, 0.03, 1.0),
}

# ---------------------------------------------------------------------------
# Instrument layout (ratios relative to widget dimensions)
# ---------------------------------------------------------------------------
NUM_STRINGS = 8

# Vertical extent of strings within the lyre widget
STRING_AREA_TOP_RATIO    = 0.15   # fraction of widget height from top
STRING_AREA_BOTTOM_RATIO = 0.82   # fraction of widget height from top

# Left/right margin for the string area
STRING_MARGIN_RATIO = 0.12        # fraction of widget width on each side

# Resonator (lower body) dimensions
RESONATOR_HEIGHT_RATIO = 0.30     # fraction of widget height
RESONATOR_TOP_RATIO    = 0.70     # fraction of widget height where body starts

# Arm width in pixels
ARM_WIDTH_PX = 18

# Crossbar height in pixels
CROSSBAR_HEIGHT_PX = 16

# String thickness (px) indexed 0 (lowest) → 7 (highest)
STRING_THICKNESSES_PX = [6.0, 5.5, 5.0, 4.5, 4.0, 3.5, 3.0, 2.5]

# Invisible hitbox half-width in pixels (per string)
STRING_HITBOX_HALF_WIDTH_PX = 34

# ---------------------------------------------------------------------------
# Gesture thresholds
# ---------------------------------------------------------------------------
TAP_DRIFT_PX       = 18     # max movement to still count as a tap
HOLD_DRIFT_PX      = 22     # max drift while waiting for hold activation
HOLD_THRESHOLD_MS  = 150    # ms before a stationary touch becomes a mute-hold
MIN_SWIPE_PX       = 25     # minimum movement to trigger swipe detection

# ---------------------------------------------------------------------------
# Audio
# ---------------------------------------------------------------------------
SAMPLE_RATE     = 44100    # Hz
SAMPLE_DEPTH    = 2        # bytes (16-bit)
POLYPHONY       = 16       # max simultaneous voices

ADSR = {
    "attack":  0.010,   # seconds
    "decay":   0.18,    # seconds
    "sustain": 0.35,    # level (0–1)
    "release": 0.50,    # seconds
}

SAMPLE_DURATION_S = 4.0    # length of each generated sample

# Maximum sympathetic resonance amplitude (fraction of source)
SYMPATHETIC_MAX = 0.15

# ---------------------------------------------------------------------------
# UI
# ---------------------------------------------------------------------------
APP_TITLE    = "Davidic Lyre"
TOP_BAR_H    = 56     # px
BOTTOM_BAR_H = 72     # px

# Default toggle states
DEFAULT_LABELS_ON  = False
DEFAULT_DRONE_ON   = False
DEFAULT_LEFT_HAND  = False
DEFAULT_REVERB     = 0.15   # 0.0–1.0
DEFAULT_MUTE_SENS  = 0.5    # 0.0–1.0 (maps to hold threshold multiplier)

# Vibration animation
VIBRATION_FRAMES    = 30    # frames per pluck animation cycle
VIBRATION_MAX_AMP   = 8     # pixels side-to-side max
VIBRATION_DECAY     = 0.92  # per-frame decay factor
