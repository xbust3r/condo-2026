from enum import Enum


class CondominiumSuccessMessage(str, Enum):
    CREATED = "Condominium created successfully"
    RETRIEVED = "Condominium retrieved successfully"
    UPDATED = "Condominium updated successfully"
    DELETED = "Condominium deleted successfully (soft delete)"
    LISTED = "Condominiums listed successfully"
    RESTORED = "Condominium restored successfully"