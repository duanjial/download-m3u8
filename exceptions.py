from abstract_exception import AbstractException


class OverLimitException(AbstractException):
    def __init__(self, message=""):
        super().__init__(message)


class VideoTypeNotSupportException(AbstractException):
    def __init__(self, message=""):
        super().__init__(message)


class UnableToClickException(AbstractException):
    def __init__(self, message=""):
        super().__init__(message)
