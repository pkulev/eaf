"""Base renderer definitions."""

from __future__ import annotations

import typing
from abc import ABCMeta
from typing import List, Optional

from eaf.obj import Object


if typing.TYPE_CHECKING:
    from eaf.core import Vec3


class Image(metaclass=ABCMeta):
    """Base image class.

    Image must implement protocol between Renderer and Renderable itself.
    """


class Renderable(Object):
    """Base class for renderable objects."""

    render_priority: int = 0
    """Priority for renderer, greater -> rendered later."""

    def __init__(self, pos: Optional[Vec3] = None):
        super().__init__(pos)

        # Image is not required by constructor, but renderable entity should
        # provide it via setter or directly assign to _image.
        self._image: Optional[Image] = None

    @property
    def image(self) -> Image:
        return self._image

    @image.setter
    def image(self, image: Image):
        self._image = image


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
