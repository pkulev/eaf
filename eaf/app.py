"""Base application class for all your needs.

Only one application can exist in one interpreter instance.
You can use instance of this class without being inherited, but expect reduced
functionality.
"""

from __future__ import annotations

import typing
import weakref

# TODO: move out into ioloop integration framework
from tornado import ioloop

import eaf.core
import eaf.errors
from eaf.clock import Clock
from eaf.render import Renderer


if typing.TYPE_CHECKING:
    from eaf.state import State  # pragma: no cover


class Application:
    """Base application class.

    Provides state manipulation routines. Subclasses are required to provide
    renderer and event queue because there is no enterprise solutions without
    input and output.
    """

    __instance__ = None
    """Instance of the current application."""

    def __init__(
        self,
        renderer: Renderer | None = None,
        event_queue: None = None,  # TODO: implement event queue abstraction
        fps: int = 30,
    ) -> None:
        self._renderer = renderer or Renderer("dummy")
        self._event_queue = event_queue

        self._state: State | None = None
        self._states: dict[str, State] = {}
        self._fps = fps

        self._clock = Clock()
        self._frames = 0

        self._ioloop = ioloop.IOLoop.current()
        tick = weakref.WeakMethod(self.tick)
        self._pc = ioloop.PeriodicCallback(tick(), fps)
        self._pc.start()

        if Application.__instance__ is None or Application.__instance__() is None:
            Application.__instance__ = weakref.ref(self)

    def tick(self) -> None:
        """Executes every frame."""

        if not self._state:
            return

        dt = self._clock.tick()

        self._state.events()
        self._state.update(dt)
        self._state.render()

        self._frames += 1

    @classmethod
    def current(cls) -> Application:
        """Return the current application instance."""

        if cls.__instance__ is None:
            raise eaf.errors.ApplicationNotInitializedError()

        application = cls.__instance__()

        if application is None:
            raise eaf.errors.ApplicationNotInitializedError()

        return application

    @property
    def state(self) -> State:
        """Current state getter."""

        if self._state:
            return self._state
        else:
            raise eaf.errors.ApplicationIsEmpty()

    @state.setter
    def state(self, name: str) -> None:
        """Current state setter."""

        if name in self._states:
            self._state = self._states[name]
        else:
            raise eaf.errors.ApplicationStateIsNotRegistered(name)

    @property
    def states(self) -> dict[str, State]:
        """State names to State classes mapping."""

        return self._states

    def register(self, state: type[State]) -> None:
        """Add new state and initiate it with owner application.

        :param state: state class to register
        """

        name = state.__name__
        state_object = state(self)
        self._states[name] = state_object

        # NOTE: State cannot instantiate in State.__init__ objects that
        #       want access to state because there is no instance at creation
        #       moment. For such objects state can declare it's 'postinit'
        #       method.
        # NOTE: Objects in state on postinit phase can try access current
        #       state, so it must be used as current at postinit state, and
        #       rolled back after.
        previous_state = self._state
        self._state = self._states[name]

        state_object.postinit()

        if len(self._states) > 1:
            self._state = previous_state

    def deregister(self, name: str) -> None:
        """Remove existing state."""

        state = self._states.pop(name)
        del state

    def trigger_state(self, state: str, *args, **kwargs) -> None:
        """Change current state and pass args and kwargs to it."""

        self.state = state  # type: ignore
        self.state.trigger(*args, **kwargs)

    def trigger_reinit(self, name: str) -> None:
        """Deregister state, register again and make it current."""

        state = self.states[name].__class__

        self.deregister(name)
        self.register(state)
        self.state = name  # type: ignore

    @property
    def renderer(self) -> Renderer:
        """Application's renderer getter."""

        return self._renderer

    @property
    def event_queue(self) -> None:
        """Application's event queue getter."""

        return self._event_queue

    @property
    def fps(self) -> int:
        """Desired FPS getter."""

        return self._fps

    @fps.setter
    def fps(self, val: int) -> None:
        """Desired FPS setter."""

        self._fps = int(val)

    @property
    def frame_count(self) -> int:
        """The total number of frames have passed from the application start."""

        return self._frames

    @property
    def clock(self) -> Clock:
        """Return clock object used by Application."""

        return self._clock

    def start(self) -> None:
        """Start main application loop."""

        if not self._state:
            raise eaf.errors.ApplicationIsEmpty()

        self._ioloop.start()

    def stop(self) -> None:
        """Stop application."""

        self._pc.stop()
        self._ioloop.add_callback(self._ioloop.stop)


def current() -> Application:
    """Current application getter."""

    return Application.current()
