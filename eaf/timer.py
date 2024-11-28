"""Simple timer that must be updated in loop."""

from collections.abc import Callable


class Timer:
    """Simple timer, calls callback when time's up. Doesn't have own loop."""

    def __init__(self, end_time: int | float, func: Callable[[], None]) -> None:
        self._end = float(end_time)
        self._func = func
        self._start = 0.0
        self._current = self._start
        self._running = False

    def _tick(self, dt: int) -> None:
        """Refresh counter."""

        if self.running:
            self._current += dt / 1000

    def _time_is_up(self) -> bool:
        """return is it time to fire fuction or not."""

        return self._current - self._start >= self._end

    def start(self) -> None:
        """Start timer."""

        self._running = True
        self._start = 0.0
        self._current = 0.0

    def stop(self) -> None:
        """Stop timer."""

        self._running = False

    def restart(self) -> None:
        """Restart timer."""

        self._start = 0.0
        self._current = 0.0
        self.start()

    def reset(self) -> None:
        """Reset timer."""

        self._running = False
        self._start = 0.0
        self._current = 0.0

    def update(self, dt: int) -> None:
        """Public method for using in loops."""

        if not self.running:
            return

        # Timer's accuracy depends on owner's loop
        self._tick(dt)
        if self._time_is_up() and self.running:
            self._func()
            self.stop()

    @property
    def running(self) -> bool:
        """Whether timer running or not."""

        return self._running

    @property
    def elapsed(self) -> float:
        """Elapsed time from start."""

        return self._current - self._start

    @property
    def remaining(self) -> float:
        """Remaining time to fire callback."""

        return self._end - self.elapsed

    def fire_function(self) -> None:
        """Call stored callback."""

        self._func()
