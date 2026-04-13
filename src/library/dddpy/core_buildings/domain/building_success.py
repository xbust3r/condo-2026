from enum import Enum


class BuildingSuccessMessage(str, Enum):
    CREATED = "Building created successfully"
    RETRIEVED = "Building retrieved successfully"
    UPDATED = "Building updated successfully"
    DELETED = "Building deleted successfully (soft delete)"
    LISTED = "Buildings listed successfully"
    RESTORED = "Building restored successfully"
    LIST_BY_CONDOMINIUM = "Buildings listed by condominium successfully"