from library.dddpy.shared.decorators.domain_exception import DomainException


class UnitNotFound(DomainException):
    def __init__(self, message: str = "Unit not found"):
        super().__init__(message, status_code=404)


class RepeatedUnitUnitNumber(DomainException):
    def __init__(self):
        super().__init__("Unit number already exists in this building", status_code=409)


class RepeatedUnitCode(DomainException):
    def __init__(self):
        super().__init__("Unit code already exists in this building", status_code=409)


class UnitHasActiveResidents(DomainException):
    def __init__(self, unit_id: int):
        super().__init__(
            f"Unit {unit_id} has active residents and cannot be physically deleted",
            status_code=409,
        )


class InvalidUnitData(DomainException):
    def __init__(self, message: str):
        super().__init__(message, status_code=400)


class BuildingNotFoundForUnit(DomainException):
    def __init__(self):
        super().__init__("Building not found for the specified unit", status_code=400)


class UnitTypeNotFound(DomainException):
    def __init__(self):
        super().__init__("Unit type not found", status_code=400)


class OccupancyStatusNotAllowed(DomainException):
    def __init__(self, status: str):
        valid = {"vacant", "occupied", "reserved", "maintenance", "blocked"}
        super().__init__(
            f"Occupancy status '{status}' is not allowed. Valid values: {', '.join(sorted(valid))}",
            status_code=400,
        )