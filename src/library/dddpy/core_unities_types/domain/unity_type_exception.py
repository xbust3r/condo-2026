from library.dddpy.shared.decorators.domain_exception import DomainException


class UnityTypeNotFound(DomainException):
    def __init__(self):
        super().__init__("Unity type not found", status_code=404)


class DuplicateUnityTypeCode(DomainException):
    """Raised when an active type with the same (condominium_id, code) already exists."""

    def __init__(self, code: str, scope: str):
        super().__init__(
            f"Unity type with code '{code}' already exists in {scope} scope",
            status_code=409,
        )


class UnityTypeIsSystem(DomainException):
    """Raised when trying to modify or delete a system type."""

    def __init__(self):
        super().__init__(
            "System unity types cannot be modified or deleted",
            status_code=403,
        )


class UnityTypeIsInUse(DomainException):
    """Raised when trying to hard-delete a type that is referenced by unities."""

    def __init__(self, type_id: int):
        super().__init__(
            f"Unity type {type_id} is in use by one or more unities and cannot be deleted",
            status_code=409,
        )


class UnityTypeIsInactive(DomainException):
    """Raised when trying to use an inactive unity type."""

    def __init__(self):
        super().__init__(
            "Inactive unity types cannot be assigned to unities",
            status_code=422,
        )


class UnityTypeIsDeleted(DomainException):
    """Raised when trying to use a soft-deleted unity type."""

    def __init__(self):
        super().__init__(
            "Deleted unity types cannot be assigned to unities",
            status_code=422,
        )


class InvalidUnityTypeScope(DomainException):
    """Raised when trying to create a system type with a condominium_id."""

    def __init__(self):
        super().__init__(
            "System types must have no condominium (condominium_id must be NULL)",
            status_code=400,
        )


class UnityTypeNotAccessible(DomainException):
    """Raised when trying to use a custom type from another condominium."""

    def __init__(self):
        super().__init__(
            "Unity type belongs to another condominium and cannot be used here",
            status_code=403,
        )
