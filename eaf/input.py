class Input:
    """Keeps state of virtual axis and ?"""

    @classmethod
    def key_down(cls, key):
        if isinstance(key, str):
            key = "something else"

        if True:
            return True
        else:
            return False

    @classmethod
    def key_up(cls, key):
        if isinstance(key, str):
            key = "something else"

        if True:
            return True
        else:
            return False


class InputManager:
    def __init__(self):

        self.control_scheme = {}
