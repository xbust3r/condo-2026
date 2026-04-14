from library.dddpy.shared.decorators.domain_exception import DomainException


class UnityNotFound(DomainException):
    def __init__(self):
        super().__init__("Unity not found", status_code=404)


class RepeatedUnityUnitNumber(DomainException):
    def __init__(self):
        super().__init__("Unit number already exists in this building", status_code=409)


class RepeatedUnityCode(DomainException):
    def __init__(self):
        super().__init__("Unity code already exists in this building", status_code=409)


class UnityHasActiveResidents(DomainException):
    def __init__(self, unity_id: int):
        super().__init__(
            f"Unity {unity_id} has active residents and cannot be physically deleted",
            status_code=409,
        )


class InvalidUnityData(DomainException):
    def __init__(self, message: str):
        super().__init__(message, status_code=400)


class BuildingNotFoundForUnity(DomainException):
    def __init__(self):
        super().__init__("Building not found for the specified unity", status_code=400)


class UnityTypeNotFound(DomainException):
    def __init__(self):
        super().__init__("Unity type not found", status_code=400)


class OccupancyStatusNotAllowed(DomainException):
    def __init__(self, status: str):
        valid = {"vacant", "occupied", "reserved", "maintenance", "blocked"}
        super().__init__(
            f"Occupancy status '{status}' is not allowed. Valid values: {', '.join(sorted(valid))}",
            status_code=400,
        )
