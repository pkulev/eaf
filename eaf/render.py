"""Base renderer definitions."""

from __future__ import annotations

import typing


if typing.TYPE_CHECKING:
    from eaf.core import Vec3


class Image:
    """Base image class.

    Image must implement protocol between Renderer and Renderable itself.
    """


class Renderable:
    """Base class for renderable objects.

    .. class-variables::

    * compound:
    * render_priority: priority for renderer, greater -> rendered later
    """

    # TODO: this is not the place
    compound: bool = False
    """Whether an object consists of other renderables."""

    render_priority: int = 0
    """A priority value for renderer, greater -> rendered later."""

    def __init__(self, pos: Vec3) -> None:
        self._pos = pos

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

    @property
    def type(self) -> str:
        return self.__class__.__name__

    # TODO: this is not the place too
    def get_renderable_objects(self) -> list[Renderable]:
        """If object is compound it must return its renderable objects."""

        raise NotImplementedError()


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
