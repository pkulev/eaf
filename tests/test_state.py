"""Tests for eaf.state module."""


import pytest

from eaf.state import State


def test_state(mock_application):
    app = mock_application()
    state = State(app)

    assert state.app is app
    assert state.actor is None

    assert not state.postinit()
    assert not state.trigger()

    with pytest.raises(NotImplementedError):
        state.events()

    assert not state.update(0)
    assert not state.render()

    assert state._objects == []
    # TODO: add tests for add and remove
