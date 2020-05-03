"""Default clock implementation."""

import time


class Clock:
    """Object that helps to track time.

    All calculations are performed in milliseconds.
    """

    FPS_COUNT_NUMBER = 10
    """Number of FPS values to keep for calculating average FPS."""

    def __init__(self):
        self._mspf = 0
        self._previous_tick = 0
        self._current_tick = self._get_ticks_ms()
        self._tick_time = 0
        self._fps_values = []

    @staticmethod
    def _get_ticks_ms():
        """Return ticks clock are rely on."""

        return int(time.monotonic() * 1000)

    def _save_fps(self, value: int):
        """Save FPS value and crop list if needed."""

        self._fps_values.append(value)
        if len(self._fps_values) > self.FPS_COUNT_NUMBER:
            self._fps_values.pop(0)

    def tick(self, framerate=0.0):
        """Update the clock.

        :param float framerate: expected FPS
        """

        self._previous_tick = self._current_tick
        self._current_tick = self._get_ticks_ms()
        delta = self._current_tick - self._previous_tick

        self._mspf = int(1.0 / framerate * 1000.0) if framerate else delta

        time_s = (self._mspf - delta) / 1000.0
        time.sleep(time_s)

        self._tick_time = self._get_ticks_ms() - self._previous_tick
        self._save_fps(int(1000 / self._tick_time) if self._tick_time != 0 else 0)

        return self._tick_time

    @property
    def fps(self) -> int:
        """Compute the clock framerate.

        :return: FPS
        :rtype: float
        """

        if not self._fps_values:
            return 0

        return int(sum(self._fps_values) / len(self._fps_values))

    @property
    def delta(self) -> int:
        """Time used in previous tick.

        :return: tick duration in milliseconds
        :rtype: int
        """
        return self._tick_time
