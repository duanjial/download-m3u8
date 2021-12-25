from abc import ABC


class AbstractException(ABC, Exception):
    def __init__(self, message=""):
        self._message = message
        super().__init__(self._message)

    def get_msg(self):
        return self._message
