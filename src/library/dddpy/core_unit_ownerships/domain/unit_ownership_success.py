from enum import Enum


class UnitOwnershipSuccessMessage(str, Enum):
    CREATED = "Unit ownership created successfully"
    RETRIEVED = "Unit ownership retrieved successfully"
    UPDATED = "Unit ownership updated successfully"
    DELETED = "Unit ownership deleted successfully (soft delete)"
    LISTED = "Unit ownerships listed successfully"
    RESTORED = "Unit ownership restored successfully"
    LIST_BY_UNIT = "Unit ownerships listed by unit successfully"
    LIST_BY_USER = "Unit ownerships listed by user successfully"
