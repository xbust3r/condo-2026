from library.dddpy.shared.decorators.domain_exception import DomainException


class UnitOccupancyNotFound(DomainException):
    def __init__(self):
        super().__init__("Unit occupancy not found", status_code=404)


class DuplicateOccupancyRecord(DomainException):
    def __init__(self):
        super().__init__(
            "An active occupancy record already exists for this unit, user and occupancy_type",
            status_code=409,
        )


class OccupancyTypeNotFoundInCatalog(DomainException):
    def __init__(self, occupancy_type_id: int):
        super().__init__(
            f"Occupancy type id={occupancy_type_id} not found or inactive in catalog",
            status_code=400,
        )


class InvalidOccupancyStatus(DomainException):
    def __init__(self, status: str):
        valid = {"active", "inactive", "historical", "pending"}
        super().__init__(
            f"Status '{status}' is not allowed. Valid values: {', '.join(sorted(valid))}",
            status_code=400,
        )


class UnitNotFoundForOccupancy(DomainException):
    def __init__(self):
        super().__init__("Unit not found for the specified unit_id", status_code=400)


class UserNotFoundForOccupancy(DomainException):
    def __init__(self):
        super().__init__("User not found for the specified user_id", status_code=400)


class UnauthorizedOccupancy(DomainException):
    def __init__(self):
        super().__init__(
            "User not authorized to create this occupancy record",
            status_code=403,
        )


class PrimaryOccupancyConflict(DomainException):
    def __init__(self):
        super().__init__(
            "Another primary occupancy already exists for this unit",
            status_code=409,
        )
