"""Provides basic Application state class."""

from __future__ import annotations

import logging
import typing
from operator import attrgetter


if typing.TYPE_CHECKING:
    from eaf.app import Application
    from eaf.core import Object
    from eaf.render import Renderable


LOG = logging.getLogger(__name__)


class State:
    """Base class for application states.

    State is a container for objects. User should add and remove objects via
    state methods. Other systems (e.g. collision or animation) must carefully
    refer to state objects to not cause memory leaks.
    """

    def __init__(self, app: Application) -> None:
        LOG.info("Instantiating %s state.", self.__class__.__name__)

        self._app = app
        self._actor = None

        # TODO: Object, not nescessarily Renderable!
        self._objects: list[Object] = []
        self._renderable: list[Renderable] = []

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

    def events(self) -> None:
        """Event handler, called by `Application.loop` method."""

        raise NotImplementedError()

    def update(self, dt: int) -> None:
        """Update handler, called every frame."""

        for obj in self._objects:
            obj.update(dt)

    def render(self) -> None:
        """Render handler, called every frame."""

        self.app.renderer.clear()
        self.app.renderer.render_objects(self._objects)
        self.app.renderer.present()

    # TODO: [object-system]
    #  * implement GameObject common class for using in states
    #  * generalize interaction with game objects and move `add` to base class
    # ATTENTION: renderables that added by another objects in runtime will not
    #  render at the screen, because they must register in state via this func
    #  as others. This is temporary decision as attempt to create playable game
    #  due to deadline.
    def add(self, obj: Renderable | list[Renderable]) -> None:
        """Add Object to State's list of objects.

        State will call Object.update() and pass to the renderer all renderables every frame.
        """

        obj = list(obj) if isinstance(obj, list) else [obj]
        self._objects += obj
        LOG.debug(f"Adding {obj} to state {self}")

        # TODO: Because we don't have common GameObject interface
        # This is temporary smellcode
        for item in obj:
            if item.compound:
                subitems = item.get_renderable_objects()
                LOG.debug(f"Adding subitems: {subitems}")
                self._objects += subitems

        self._objects.sort(key=attrgetter("render_priority"))

    def remove(self, obj: Renderable) -> None:
        """Remove object from State's list of objects.

        Removed objects should be collected by GC.
        """

        LOG.debug("%s", obj)

        try:
            if obj.compound:
                for subobj in obj.get_renderable_objects():
                    self._objects.remove(subobj)
                    del subobj
            self._objects.remove(obj)
        except ValueError:
            LOG.exception("Object %s is not in State's object list.", obj)
        finally:
            del obj

    def __str__(self) -> str:
        return f"{self.__class__.__name__}"
