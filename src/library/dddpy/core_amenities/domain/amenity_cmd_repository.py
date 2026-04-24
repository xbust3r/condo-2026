"""
Amenity command repository interface — DDD domain layer.
"""


class AmenityCmdRepository:
    """Interface for write operations on amenities."""

    def create(self, entity: object) -> int:
        pass

    def update(self, entity: object) -> bool:
        pass

    def soft_delete(self, id: int) -> bool:
        pass

    def hard_delete(self, id: int) -> bool:
        pass
