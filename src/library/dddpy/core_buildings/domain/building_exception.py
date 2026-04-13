from library.dddpy.shared.decorators.domain_exception import DomainException


class BuildingNotFound(DomainException):
    def __init__(self):
        super().__init__("Building not found", status_code=404)


class RepeatedBuildingCode(DomainException):
    def __init__(self):
        super().__init__("Building code already exists in this condominium", status_code=409)


class BuildingHasActiveUnits(DomainException):
    def __init__(self, building_id: int):
        super().__init__(f"Building {building_id} has active units and cannot be physically deleted", status_code=409)


class InvalidBuildingData(DomainException):
    def __init__(self, message: str):
        super().__init__(message, status_code=400)


class CondominiumNotFoundForBuilding(DomainException):
    def __init__(self):
        super().__init__("Condominium not found for the specified building", status_code=400)


class BuildingTypeNotFound(DomainException):
    def __init__(self):
        super().__init__("Building type not found", status_code=400)