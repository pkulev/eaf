"""Signal implementation."""

from typing import Callable, List


class Signal:
    """Signal representation.

    Stores callbacks, added via `connect` and calls all of them on `emit`.
    """

    def __init__(self):
        self._callbacks: List[Callable] = []

    def connect(self, func: Callable):
        """Connect `func` with signal."""

        self._callbacks.append(func)

    def disconnect(self, func: Callable):
        """Disconnect `func` from signal."""

        try:
            self._callbacks.remove(func)
        except ValueError:
            pass

    def emit(self, *args, **kwargs):
        """Emit signal to all it's callbacks."""

        for callback in self._callbacks:
            callback(*args, **kwargs)
