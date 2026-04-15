"""
User profile exceptions.
"""


class UserProfileException(Exception):
    pass


class UserProfileNotFound(UserProfileException):
    pass


class UserProfileAlreadyExists(UserProfileException):
    pass
