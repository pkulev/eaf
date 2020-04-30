"""Base renderer definitions."""

from __future__ import annotations

import typing

from abc import ABCMeta, abstractmethod
from typing import List


if typing.TYPE_CHECKING:
    from eaf.core import Vec3


class Renderable(metaclass=ABCMeta):
    """Base class for renderable objects.

    .. class-variables::

    * compound (bool): if object consists of other renderables

    * render_priority (int): priority for renderer, greater -> rendered later

    * draw_on_border (bool): allow or not drawing on border
    if not allowed - renderer will send remove_obsolete signal to object
    """

    # TODO: this is not the place
    compound = False
    render_priority = 0
    # TODO: this is not the place too (ncurses-specific)
    draw_on_border = False

    def __init__(self):
        self._image = None

    # TODO: Renderable must return some object with clean interface
    @abstractmethod
    def get_render_data(self):
        """Renderable.get_render_data(None) -> (gpos_list, data_gen)

        Every renderable object must return tuple consist of:
            * gpos_list: list of every Surface's global positions
            Example: [Vec3(x=5, y=5), Vec3(x=10, y=10)]

            * data_gen: generator which yields tuple (lpos, image, style)
            Example: (Vec3(x=5, y=5), "*", curses.A_BOLD)
        """
        pass

    # TODO: this is the wrong place
    @classmethod
    def type(cls):
        return cls.__name__

    # TODO: fix sometimes
    @property
    def image(self):
        return self._image

    # TODO: this is bad designed thing
    def remove_obsolete(self, pos: Vec3):
        """Remove obsolete signal.

        Every renderable object must remove old bullets that places behind
        border (field for rendering).

        If object will never change its coordinates it may not implement this
        method.
        """

        pass

    # TODO: this is not the place too
    def get_renderable_objects(self) -> List[Renderable]:
        """If object is compound it must return its renderable objects."""

        pass


class Renderer:
    """Base renderer class. Instance can be used as dummy renderer.

    Each renderer have screen to render to. This is the only assumption this
    class makes.
    """

    def __init__(self, screen):
        self._screen = screen

    @property
    def screen(self):
        return self._screen

    def clear(self):
        pass

    def render_objects(self, objects: List[Renderable]):
        pass

    def present(self):
        pass

    def get_width(self):
        pass

    def get_height(self):
        pass
