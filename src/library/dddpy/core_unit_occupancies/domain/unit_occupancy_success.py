from enum import Enum


class UnitOccupancySuccessMessage(str, Enum):
    CREATED = "Unit occupancy created successfully"
    RETRIEVED = "Unit occupancy retrieved successfully"
    UPDATED = "Unit occupancy updated successfully"
    DELETED = "Unit occupancy deleted successfully (soft delete)"
    LISTED = "Unit occupancies listed successfully"
    RESTORED = "Unit occupancy restored successfully"
    LIST_BY_UNIT = "Unit occupancies listed by unit successfully"
    LIST_BY_USER = "Unit occupancies listed by user successfully"
    HARD_DELETED = "Unit occupancy permanently deleted"
