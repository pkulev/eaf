"""Base renderer definitions."""

from __future__ import annotations

import typing
from abc import ABCMeta
from typing import List, Optional

from eaf.obj import Object


if typing.TYPE_CHECKING:
    from eaf.core import Vec3


class Image:
    """Base image class.

    Image must implement protocol between Renderer and Renderable itself.
    """


class Renderable(Object):
    """Base class for renderable objects."""

    render_priority: int = 0
    """Priority for renderer, greater -> rendered later."""

    def __init__(self, pos: Vec3 | None = None) -> None:
        super().__init__(pos)

        # Image is not required by constructor, but renderable entity should
        # provide it via setter or directly assign to _image.
        self._image: Image | None = None

    @property
    def pos(self) -> Vec3:
        return self._pos

    @pos.setter
    def pos(self, pos: Vec3) -> None:
        self._pos = pos

    @property
    def image(self) -> Image:
        """Image getter."""

        if self._image is None:
            raise ValueError("Image property must be set before accessing!")

        return self._image

    @image.setter
    def image(self, image: Image) -> None:
        """Image setter."""

        self._image = image


class Renderer:
    """Base renderer class. Instance can be used as dummy renderer.

    Each renderer have screen to render to. This is the only assumption this
    class makes.
    """

    def __init__(self, screen) -> None:
        self._screen = screen

    @property
    def screen(self):
        return self._screen

    def clear(self) -> None:
        pass

    def render_objects(self, objects: list[Renderable]) -> None:
        pass

    def present(self) -> None:
        pass

    def get_width(self) -> None:
        pass

    def get_height(self) -> None:
        pass
