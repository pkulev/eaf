"""Provides basic Application state class."""

from __future__ import annotations

import logging
import typing

from typing import List, Sequence, Union, Iterable


if typing.TYPE_CHECKING:
    from eaf.app import Application
    from eaf.render import Renderer, Renderable


LOG = logging.getLogger(__name__)


class State:
    """Base class for application states.

    State is a container for objects. User should add and remove objects via
    state methods. Other systems (e.g. collision or animation) must carefully
    refer to state objects to not cause memory leaks.
    """

    def __init__(self, app: Application):
        LOG.info("Instantiating %s state.", self.__class__.__name__)

        self._app = app
        self._renderer: Renderer = app.renderer
        self._actor = None

        self._objects: List[Renderable] = []

    def postinit(self):
        """Do all instantiations that require prepared State object."""

        LOG.debug("Post init %s state.", self.__class__.__name__)

    def trigger(self, *args, **kwargs):
        """Common way to get useful information for triggered state."""

        LOG.debug(
            "Triggering %s state with %s and %s", self.__class__.__name__, args, kwargs
        )

    @property
    def app(self) -> Application:
        """State's owner getter."""
        return self._app

    @property
    def actor(self) -> object:
        """Controllable object getter."""
        return self._actor

    @actor.setter
    def actor(self, val):
        """Controllable object setter."""

        self._actor = val

    def events(self):
        "Event handler, called by `Application.loop` method."
        raise NotImplementedError

    def update(self):
        """Update handler, called every frame."""

        for obj in self._objects:
            obj.update()

    def render(self):
        """Render handler, called every frame."""

        self._renderer.clear()
        self._renderer.render_objects(self._objects)
        self._renderer.present()

    # TODO: [object-system]
    #  * implement GameObject common class for using in states
    #  * generalize interaction with game objects and move `add` to base class
    # ATTENTION: renderables that added by another objects in runtime will not
    #  render at the screen, because they must register in state via this func
    #  as others. This is temporary decision as attempt to create playable game
    #  due to deadline.
    def add(self, obj: Union[Renderable, List[Renderable]]):
        """Add GameObject to State's list of objects.

        State will call GameObject.update() and pass to render all it's objects
        every frame.
        """

        obj = list(obj) if isinstance(obj, list) else [obj]
        self._objects += obj
        LOG.debug("%s", obj)

        # TODO: Because we don't have common GameObject interface
        # This is temporary smellcode
        for item in obj:
            if item.compound:
                subitems = item.get_renderable_objects()
                LOG.debug("Subitems: %s", subitems)
                self._objects += subitems

    def remove(self, obj: Renderable):
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
