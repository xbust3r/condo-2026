"""
OccupancyType exceptions.
"""


class OccupancyTypeNotFound(Exception):
    """Raised when an occupancy type is not found."""
    pass


class OccupancyTypeAlreadyExists(Exception):
    """Raised when trying to create a code that already exists."""
    pass


class OccupancyTypeCodeRequired(Exception):
    """Raised when code is missing on create."""
    pass