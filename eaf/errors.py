"""EAF error definitions."""


class Error(Exception):
    """Base class for all EAF exceptions."""


class ApplicationNotInitializedError(Error):
    """Raise when try to get not initialized application."""

    def __init__(self):
        super().__init__("Application not initialized.")


class ApplicationIsEmpty(Error):
    """Raise when try to get state from empty application."""

    def __init__(self):
        super().__init__("Application has no registered states.")


class ApplicationStateIsNotRegistered(Error):
    """Raise when try to get state which was not registered."""

    def __init__(self, name: str):
        super().__init__(f"State '{name}' is not registered.")
