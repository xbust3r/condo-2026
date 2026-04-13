from library.dddpy.shared.decorators.domain_exception import DomainException


class BuildingTypeNotFound(DomainException):
    def __init__(self):
        super().__init__("Building type not found", status_code=404)


class DuplicateBuildingTypeCode(DomainException):
    """Raised when an active type with the same (condominium_id, code) already exists."""
    def __init__(self, code: str, scope: str):
        super().__init__(
            f"Building type with code '{code}' already exists in {scope} scope",
            status_code=409,
        )


class BuildingTypeIsSystem(DomainException):
    """Raised when trying to modify or delete a system type."""
    def __init__(self):
        super().__init__(
            "System building types cannot be modified or deleted",
            status_code=403,
        )


class BuildingTypeIsInUse(DomainException):
    """Raised when trying to hard-delete a type that is referenced by buildings."""
    def __init__(self, type_id: int):
        super().__init__(
            f"Building type {type_id} is in use by one or more buildings and cannot be deleted",
            status_code=409,
        )


class BuildingTypeIsInactive(DomainException):
    """Raised when trying to use an inactive building type."""
    def __init__(self):
        super().__init__(
            "Inactive building types cannot be assigned to buildings",
            status_code=422,
        )


class BuildingTypeIsDeleted(DomainException):
    """Raised when trying to use a soft-deleted building type."""
    def __init__(self):
        super().__init__(
            "Deleted building types cannot be assigned to buildings",
            status_code=422,
        )


class InvalidBuildingTypeScope(DomainException):
    """Raised when trying to create a system type with a condominium_id."""
    def __init__(self):
        super().__init__(
            "System types must have no condominium (condominium_id must be NULL)",
            status_code=400,
        )


class BuildingTypeNotAccessible(DomainException):
    """Raised when trying to use a custom type from another condominium."""
    def __init__(self):
        super().__init__(
            "Building type belongs to another condominium and cannot be used here",
            status_code=403,
        )
