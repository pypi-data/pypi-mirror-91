"""

ro.py > errors.py

This file houses custom exceptions unique to this module.

"""


class NotLimitedError(Exception):
    """Called when code attempts to read limited-only information."""
    pass


class InvalidIconSizeError(Exception):
    """Called when code attempts to pass in an improper size to a thumbnail function."""
    pass


class InvalidShotTypeError(Exception):
    """Called when code attempts to pass in an improper avatar image type to a thumbnail function."""
    pass


class ApiError(Exception):
    """Called in requests when an API request fails."""
    pass


class ChatError(Exception):
    """Called in chat when a chat action fails."""


class InvalidPageError(Exception):
    """Called when an invalid page is requested."""


class NotFound(Exception):
    """Called when something is not found."""


class UserDoesNotExistError(Exception):
    """Called when a user does not exist."""


class GameJoinError(Exception):
    """Called when an error occurs when joining a game."""
