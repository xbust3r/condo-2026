from enum import Enum


class CondominiumRoleSuccessMessage(str, Enum):
    CREATED = "Condominium role created successfully"
    RETRIEVED = "Condominium role retrieved successfully"
    UPDATED = "Condominium role updated successfully"
    DELETED = "Condominium role deleted successfully (soft delete)"
    LISTED = "Condominium roles listed successfully"
    RESTORED = "Condominium role restored successfully"
    LIST_BY_CONDOMINIUM = "Condominium roles listed by condominium successfully"
    LIST_BY_USER = "Condominium roles listed by user successfully"
    HARD_DELETED = "Condominium role permanently deleted"
