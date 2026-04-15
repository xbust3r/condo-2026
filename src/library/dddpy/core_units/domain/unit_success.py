from enum import Enum


class UnitSuccessMessage(str, Enum):
    CREATED = "Unit created successfully"
    RETRIEVED = "Unit retrieved successfully"
    UPDATED = "Unit updated successfully"
    DELETED = "Unit deleted successfully (soft delete)"
    LISTED = "Units listed successfully"
    RESTORED = "Unit restored successfully"
    LIST_BY_BUILDING = "Units listed by building successfully"
    HARD_DELETED = "Unit permanently deleted"