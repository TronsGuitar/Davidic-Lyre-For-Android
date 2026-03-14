"""
app/config.py — Constants, UI dimensions, thresholds, and default presets.

Centralises all tunable values for the Davidic Lyre app so that they can be
adjusted in a single location without touching business-logic code.  Refer to
PRD Sections 8 (Interaction Specification) and 6 (color palette) for the
rationale behind these defaults.
"""

# ---------------------------------------------------------------------------
# Gesture thresholds (PRD Section 8 / Section 16)
# ---------------------------------------------------------------------------

# Maximum finger drift (px) before a touch-down is no longer considered a tap
TAP_DRIFT_PX: int = 18

# Maximum finger drift (px) while holding before the hold is cancelled
HOLD_DRIFT_PX: int = 22

# Duration (ms) a touch must remain stationary to activate hold-mute
MUTE_THRESHOLD_MS: int = 150

# Minimum swipe distance (px) required to begin registering string crossings
MIN_SWIPE_PX: int = 25

# ---------------------------------------------------------------------------
# UI dimensions
# ---------------------------------------------------------------------------

# TODO: Define lyre widget padding and proportions for Fold5 inner screen
# LYRE_PADDING_TOP_PX    = ...
# LYRE_PADDING_BOTTOM_PX = ...
# LYRE_PADDING_SIDE_PX   = ...
# STRING_SPACING_PX      = ...

# ---------------------------------------------------------------------------
# Color palette (PRD Section 6)
# ---------------------------------------------------------------------------

COLOR_LIGHT_WOOD: str = "#A87442"
COLOR_MEDIUM_WOOD: str = "#7A4E2A"
COLOR_DARK_WOOD: str = "#4A2E1A"
COLOR_HIGHLIGHT_WEAR: str = "#C99562"
COLOR_GUT_STRING_LIGHT: str = "#E8DCC8"
COLOR_GUT_STRING_DARK: str = "#9A6E45"

# ---------------------------------------------------------------------------
# Audio / envelope defaults (PRD Section 9)
# ---------------------------------------------------------------------------

# TODO: Define ADSR envelope defaults
# ATTACK_S    = 0.010   # seconds
# DECAY_S     = 0.18    # seconds
# SUSTAIN     = 0.35    # level 0–1
# RELEASE_S   = 0.50    # seconds

# TODO: Define sympathetic resonance cap
# SYMPATHETIC_MAX_AMPLITUDE = 0.15

# ---------------------------------------------------------------------------
# Polyphony
# ---------------------------------------------------------------------------

# TODO: Set maximum simultaneous voices
# MAX_VOICES = 16

# ---------------------------------------------------------------------------
# Miscellaneous
# ---------------------------------------------------------------------------

# TODO: Add frame-rate target, hitbox expansion factor, and other UI constants
