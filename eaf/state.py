"""Provides basic Application state class."""

from __future__ import annotations

import logging
import typing
from operator import attrgetter

from eaf.node import Node, Tree


if typing.TYPE_CHECKING:
    from eaf.app import Application
    from eaf.obj import Object


LOG = logging.getLogger(__name__)


class State:
    """Base class for application states.

    State is a container for objects. User should add and remove objects via
    state methods. Other systems (e.g. collision or animation) must carefully
    refer to state objects to not cause memory leaks.
    """

    def __init__(self, app: Application) -> None:
        LOG.info("Instantiating %s state.", self.__class__.__name__)
        super().__init__()

        self._app = app
        self._actor = None

        self.scene_graph = Tree()

    def postinit(self) -> None:
        """Do all instantiations that require prepared State object."""

        LOG.debug("Post init %s state.", self.__class__.__name__)

    def trigger(self, *args, **kwargs) -> None:
        """Common way to get useful information for triggered state."""

        LOG.debug("Triggering %s state with %s and %s", self.__class__.__name__, args, kwargs)

    @property
    def app(self) -> Application:
        """State's owner getter."""

        return self._app

    @property
    def actor(self) -> object:
        """Controllable object getter."""

        return self._actor

    @actor.setter
    def actor(self, val) -> None:
        """Controllable object setter."""

        self._actor = val

    @property
    def objects(self) -> list[Node]:
        """State's objects getter."""

        return list(self.scene_graph.traverse_breadth())

    def events(self) -> none:
        """Event handler, called by `Application.loop` method."""

        raise NotImplementedError()

    def update(self, dt: int) -> None:
        """Update handler, called every frame."""

        for obj in self.objects:
            obj.update(dt)

    def render(self) -> None:
        """Render handler, called every frame."""

        self.app.renderer.clear()
        self.app.renderer.render_objects(self.objects)
        self.app.renderer.present()

    # pylint: disable=arguments-differ
    def add(self, obj: Object) -> None:
        """Add GameObject to State's list of objects.

        State will call Object.update(dt) and pass to render all it's objects
        every frame.
        """

        LOG.debug("[%s] Adding %s", self, obj)
        self.scene_graph.add(obj)

        self._objects.sort(key=attrgetter("render_priority"))

    def remove(self, obj: Object) -> None:
        """Remove object from State's object tree.

        Removed objects should be collected by GC.
        """

        LOG.debug("[%s]: removing %s", self, obj)

        self.scene_graph.remove(obj)
        del obj

    def __str__(self) -> str:
        return f"{self.__class__.__name__}"
