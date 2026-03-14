"""
tests/test_gestures.py — Tests for gesture detection algorithms.

Validates the functions in :mod:`app.gestures` once they are implemented:
  - Tap detection (is_tap)
  - Hold detection (check_hold)
  - Swipe string-crossing detection (find_crossed_strings)
  - Swipe velocity calculation (get_swipe_velocity)

TODO: Replace placeholder and add real test cases in Phase 1 once the
      gesture algorithms are implemented.
"""

import pytest

from app.config import HOLD_DRIFT_PX, MUTE_THRESHOLD_MS, TAP_DRIFT_PX


# ---------------------------------------------------------------------------
# Placeholder — always passes; replace with real assertions in Phase 1
# ---------------------------------------------------------------------------


def test_placeholder():
    """Placeholder test — confirms the module imports without error."""
    # TODO: Replace with comprehensive gesture tests in Phase 1
    assert True


# ---------------------------------------------------------------------------
# Threshold constant sanity checks
# ---------------------------------------------------------------------------


def test_tap_drift_px_is_positive():
    """TAP_DRIFT_PX must be a positive integer."""
    assert isinstance(TAP_DRIFT_PX, int)
    assert TAP_DRIFT_PX > 0


def test_hold_drift_px_is_positive():
    """HOLD_DRIFT_PX must be a positive integer."""
    assert isinstance(HOLD_DRIFT_PX, int)
    assert HOLD_DRIFT_PX > 0


def test_mute_threshold_ms_is_positive():
    """MUTE_THRESHOLD_MS must be a positive integer."""
    assert isinstance(MUTE_THRESHOLD_MS, int)
    assert MUTE_THRESHOLD_MS > 0


def test_hold_drift_larger_than_tap_drift():
    """Hold drift tolerance should be at least as large as tap drift tolerance."""
    assert HOLD_DRIFT_PX >= TAP_DRIFT_PX


# ---------------------------------------------------------------------------
# Tap detection stubs (Phase 1)
# ---------------------------------------------------------------------------


@pytest.mark.skip(reason="Tap detection not yet implemented — Phase 1")
def test_is_tap_returns_true_for_short_stationary_touch():
    """A touch that moves less than TAP_DRIFT_PX and lifts early is a tap."""
    # TODO: Construct a TouchTrace and call is_tap in Phase 1
    pass


@pytest.mark.skip(reason="Tap detection not yet implemented — Phase 1")
def test_is_tap_returns_false_if_held_too_long():
    """A touch held beyond MUTE_THRESHOLD_MS should not be classified as a tap."""
    # TODO: Construct a long-held TouchTrace and assert is_tap returns False
    pass


@pytest.mark.skip(reason="Tap detection not yet implemented — Phase 1")
def test_is_tap_returns_false_if_drifted_too_far():
    """A touch that drifts beyond TAP_DRIFT_PX should not be classified as a tap."""
    # TODO: Construct a drifted TouchTrace and assert is_tap returns False
    pass


# ---------------------------------------------------------------------------
# Hold detection stubs (Phase 1)
# ---------------------------------------------------------------------------


@pytest.mark.skip(reason="Hold detection not yet implemented — Phase 1")
def test_check_hold_activates_after_threshold():
    """A stationary touch past MUTE_THRESHOLD_MS should activate hold."""
    # TODO: Construct a TouchTrace and call check_hold in Phase 1
    pass


@pytest.mark.skip(reason="Hold detection not yet implemented — Phase 1")
def test_check_hold_does_not_activate_if_moved():
    """A touch that drifts beyond HOLD_DRIFT_PX should not activate hold."""
    pass


# ---------------------------------------------------------------------------
# Swipe detection stubs (Phase 1)
# ---------------------------------------------------------------------------


@pytest.mark.skip(reason="find_crossed_strings not yet implemented — Phase 1")
def test_find_crossed_strings_detects_crossing():
    """A swipe movement crossing string hitboxes should return their IDs in order."""
    # TODO: Build LyreString list and call find_crossed_strings in Phase 1
    pass


@pytest.mark.skip(reason="get_swipe_velocity not yet implemented — Phase 1")
def test_get_swipe_velocity_basic():
    """Swipe velocity should equal distance / delta_time."""
    # TODO: Call get_swipe_velocity with known values and assert result
    pass
