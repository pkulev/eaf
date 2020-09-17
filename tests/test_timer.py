"""Tests for eaf.timer module."""

from eaf.timer import Timer


def test_timer_get_elapsed():
    timer = Timer(5.0, lambda: True)
    timer.start()
    while timer.running:
        assert timer.elapsed >= 0.0
        timer.update(13)
        assert timer.elapsed >= 0.0
