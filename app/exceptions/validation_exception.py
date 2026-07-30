"""
Validation Exception
Custom exception raised when user input validation fails
"""


class ValidationException(Exception):
    """
    Raised when user input is invalid.
    """

    def __init__(self, message: str):

        self.message = message

        super().__init__(message)