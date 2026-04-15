from enum import Enum


class UnitTypeSuccessMessage(str, Enum):
    CREATED = "Unit type created successfully"
    RETRIEVED = "Unit type retrieved successfully"
    UPDATED = "Unit type updated successfully"
    DELETED = "Unit type deleted successfully (soft delete)"
    LISTED = "Unit types listed successfully"
    RESTORED = "Unit type restored successfully"
    HARD_DELETED = "Unit type permanently deleted"