"""Base renderer definitions."""

from __future__ import annotations

import typing

from abc import ABCMeta, abstractmethod
from typing import List


if typing.TYPE_CHECKING:
    from eaf.core import Vec3


class Image(metaclass=ABCMeta):
    """Base image class.

    Image must implement protocol between Renderer and Renderable itself.
    """


class Renderable(metaclass=ABCMeta):
    """Base class for renderable objects.

    .. class-variables::

    * compound (bool): if object consists of other renderables

    * render_priority (int): priority for renderer, greater -> rendered later
    """

    # TODO: this is not the place
    compound = False
    render_priority = 0

    def __init__(self, pos: Vec3):
        self._pos = pos

        # Image is not required by constructor, but renderable entity should
        # provide it via setter or directly assign to _image.
        self._image = None

    @property
    def pos(self) -> Vec3:
        return self._pos

    @pos.setter
    def pos(self, pos: Vec3):
        self._pos = pos

    @property
    def image(self) -> Image:
        return self._image

    @image.setter
    def image(self, image: Image):
        self._image = image

    @property
    def type(self) -> str:
        return self.__class__.__name__

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
