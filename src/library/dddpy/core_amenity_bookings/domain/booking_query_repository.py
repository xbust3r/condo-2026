"""Booking query repository interface."""
from abc import ABC, abstractmethod
from typing import Optional, List, Tuple
from library.dddpy.core_amenity_bookings.domain.booking_entity import BookingEntity


class BookingQueryRepository(ABC):
    @abstractmethod
    def get_by_id(self, booking_id: int) -> Optional[BookingEntity]:
        ...

    @abstractmethod
    def get_by_uuid(self, uuid: str) -> Optional[BookingEntity]:
        ...

    @abstractmethod
    def list_all(
        self,
        condominium_id: Optional[int] = None,
        building_id: Optional[int] = None,
        amenity_id: Optional[int] = None,
        unit_id: Optional[int] = None,
        owner_id: Optional[int] = None,
        status: Optional[str] = None,
        skip: int = 0,
        limit: int = 100,
        include_deleted: bool = False,
    ) -> Tuple[List[BookingEntity], int]:
        ...

    @abstractmethod
    def find_overlapping(
        self,
        amenity_id: int,
        start_at,
        end_at,
        exclude_booking_id: Optional[int] = None,
    ) -> List[BookingEntity]:
        """Find bookings that overlap with the given time range for an amenity."""
        ...
