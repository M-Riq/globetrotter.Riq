"""
Shared application exceptions.
"""


class ValidationException(Exception):
    """Raised when user input is invalid."""

    def __init__(self, message: str):
        self.message = message
        super().__init__(message)


class NotFoundException(Exception):
    """Raised when a requested resource does not exist."""

    def __init__(self, message: str = "resource not found"):
        self.message = message
        super().__init__(message)
