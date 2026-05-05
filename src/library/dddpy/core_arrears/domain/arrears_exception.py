"""Domain exceptions for core_arrears."""


class ArrearsError(Exception):
    """Base exception for core_arrears domain."""


class UnitNotFound(ArrearsError):
    """Unit does not exist or has no arrears data."""

    def __init__(self, unit_id: int):
        super().__init__(f"No arrears data found for unit_id={unit_id}")
        self.unit_id = unit_id
