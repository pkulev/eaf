"""Tests for eaf.timer module."""

from eaf.timer import Timer


def test_timer_elapsed() -> None:
    timer = Timer(5.0, lambda: None)
    timer.start()
    while timer.running:
        assert timer.elapsed >= 0.0
        timer.update(13)
        assert timer.elapsed >= 0.0
