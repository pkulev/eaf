"""Tests for eaf.state module."""

import pytest

from eaf.state import State


def test_state(mock_application):
    app = mock_application()
    state = State(app)

    assert state.app is app
    assert state.actor is None

    state.postinit()
    state.trigger()

    with pytest.raises(NotImplementedError):
        state.events()

    state.update(0)
    state.render()

    assert state._objects == []
    # TODO: add tests for add and remove
