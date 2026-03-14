"""Constants, UI dimensions, and threshold defaults for the Davidic Lyre."""

# Touch thresholds
TAP_DRIFT_TOLERANCE = 18       # px
HOLD_DRIFT_TOLERANCE = 22      # px
HOLD_THRESHOLD = 0.15          # seconds
MIN_SWIPE_DISTANCE = 25        # px
STRING_HITBOX_WIDTH = 26       # px per side

# Velocity mapping
MIN_VELOCITY = 0.6
MAX_VELOCITY = 2.0
VELOCITY_DIVISOR = 35.0

# Vibration animation
VIBRATION_MIN = 6.0
VIBRATION_MAX = 18.0
VIBRATION_BASE = 8.0
VIBRATION_DECAY = 2.2          # amplitude multiplier decay per second
VIBRATION_FREQ = 32            # Hz visual oscillation

# Layout ratios (fraction of widget dimensions)
STRING_LEFT = 0.25
STRING_RIGHT = 0.75
STRING_TOP = 0.82
STRING_BOTTOM = 0.18

FRAME_BOTTOM_Y = 0.15
FRAME_BOTTOM_H = 0.08
FRAME_LEFT_X_BOTTOM = 0.2
FRAME_LEFT_X_TOP = 0.28
FRAME_RIGHT_X_BOTTOM = 0.8
FRAME_RIGHT_X_TOP = 0.72

# String thicknesses (low to high string, in px)
STRING_THICKNESSES = [4.5, 4.0, 3.6, 3.1, 2.7, 2.3, 2.0, 1.7]

# Color palette
COLOR_BODY = (0.48, 0.31, 0.16)
COLOR_ARM = (0.57, 0.37, 0.18)
COLOR_STRING = (0.92, 0.87, 0.78)
COLOR_STRING_MUTED = (0.55, 0.45, 0.35)
COLOR_BACKGROUND = (0.92, 0.88, 0.80, 1)

# Frame widths (px)
ARM_WIDTH = 8
CROSSBAR_WIDTH = 6

# Frame rate
TARGET_FPS = 60

# ADSR envelope (seconds / level)
ATTACK = 0.01
DECAY = 0.18
SUSTAIN = 0.35
RELEASE = 0.50
