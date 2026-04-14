from enum import Enum


class UnitySuccessMessage(str, Enum):
    CREATED = "Unity created successfully"
    RETRIEVED = "Unity retrieved successfully"
    UPDATED = "Unity updated successfully"
    DELETED = "Unity deleted successfully (soft delete)"
    LISTED = "Unities listed successfully"
    RESTORED = "Unity restored successfully"
    LIST_BY_BUILDING = "Unities listed by building successfully"
    HARD_DELETED = "Unity permanently deleted"
