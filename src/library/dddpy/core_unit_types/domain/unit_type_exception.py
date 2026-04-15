from library.dddpy.shared.decorators.domain_exception import DomainException


class UnitTypeNotFound(DomainException):
    def __init__(self):
        super().__init__("Unit type not found", status_code=404)


class DuplicateUnitTypeCode(DomainException):
    """Raised when an active type with the same (condominium_id, code) already exists."""

    def __init__(self, code: str, scope: str):
        super().__init__(
            f"Unit type with code '{code}' already exists in {scope} scope",
            status_code=409,
        )


class UnitTypeIsSystem(DomainException):
    """Raised when trying to modify or delete a system type."""

    def __init__(self):
        super().__init__(
            "System unit types cannot be modified or deleted",
            status_code=403,
        )


class UnitTypeIsInUse(DomainException):
    """Raised when trying to hard-delete a type that is referenced by units."""

    def __init__(self, type_id: int):
        super().__init__(
            f"Unit type {type_id} is in use by one or more units and cannot be deleted",
            status_code=409,
        )


class UnitTypeIsInactive(DomainException):
    """Raised when trying to use an inactive unit type."""

    def __init__(self):
        super().__init__(
            "Inactive unit types cannot be assigned to units",
            status_code=422,
        )


class UnitTypeIsDeleted(DomainException):
    """Raised when trying to use a soft-deleted unit type."""

    def __init__(self):
        super().__init__(
            "Deleted unit types cannot be assigned to units",
            status_code=422,
        )


class InvalidUnitTypeScope(DomainException):
    """Raised when trying to create a system type with a condominium_id."""

    def __init__(self):
        super().__init__(
            "System types must have no condominium (condominium_id must be NULL)",
            status_code=400,
        )


class UnitTypeNotAccessible(DomainException):
    """Raised when trying to use a custom type from another condominium."""

    def __init__(self):
        super().__init__(
            "Unit type belongs to another condominium and cannot be used here",
            status_code=403,
        )