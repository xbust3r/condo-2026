# Status constants for all modules
from enum import IntEnum


class CondominiumStatus(IntEnum):
    ACTIVE = 1
    INACTIVE = 0


class BuildingStatus(IntEnum):
    ACTIVE = 1
    INACTIVE = 0


class BuildingTypeStatus(IntEnum):
    ACTIVE = 1
    INACTIVE = 0


class UnityStatus(IntEnum):
    ACTIVE = 1
    INACTIVE = 0


class UnityTypeStatus(IntEnum):
    ACTIVE = 1
    INACTIVE = 0


class UserStatus(IntEnum):
    ACTIVE = 1
    INACTIVE = 0
    SUSPENDED = 2


class ResidentStatus(IntEnum):
    ACTIVE = 1
    INACTIVE = 0
    HISTORICAL = 2


class ResidentType(IntEnum):
    OWNER = 1
    TENANT = 2
    FAMILY = 3
    EMPLOYEE = 4
