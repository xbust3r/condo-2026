from library.dddpy.shared.decorators.domain_exception import DomainException


class UnitOwnershipNotFound(DomainException):
    def __init__(self):
        super().__init__("Unit ownership not found", status_code=404)


class DuplicateOwnershipRecord(DomainException):
    def __init__(self):
        super().__init__(
            "An active ownership record already exists for this unit and user",
            status_code=409,
        )


class OwnershipPercentageSumExceeded(DomainException):
    def __init__(self, unit_id: int, current_sum: float, additional: float):
        super().__init__(
            f"Ownership percentages for unit_id={unit_id} would exceed 100%. "
            f"Current active sum: {current_sum}%, attempting to add: {additional}%. "
            f"Total would be: {current_sum + additional}%.",
            status_code=400,
        )


class InvalidOwnershipPercentage(DomainException):
    def __init__(self, message: str):
        super().__init__(message, status_code=400)


class InvalidOwnershipType(DomainException):
    def __init__(self, ownership_type: str):
        valid = {"owner", "co_owner"}
        super().__init__(
            f"Ownership type '{ownership_type}' is not allowed. Valid values: {', '.join(sorted(valid))}",
            status_code=400,
        )


class InvalidOwnershipStatus(DomainException):
    def __init__(self, status: str):
        valid = {"active", "inactive", "historical"}
        super().__init__(
            f"Status '{status}' is not allowed. Valid values: {', '.join(sorted(valid))}",
            status_code=400,
        )


class UnitNotFoundForOwnership(DomainException):
    def __init__(self):
        super().__init__("Unit not found for the specified unit_id", status_code=400)


class UserNotFoundForOwnership(DomainException):
    def __init__(self):
        super().__init__("User not found for the specified user_id", status_code=400)
