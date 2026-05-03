"""Booking command repository interface."""
from abc import ABC, abstractmethod
from library.dddpy.core_amenity_bookings.domain.booking_entity import BookingEntity


class BookingCmdRepository(ABC):
    @abstractmethod
    def create(self, entity: BookingEntity) -> int:
        """Persist a new booking. Returns the generated id."""
        ...

    @abstractmethod
    def update(self, entity: BookingEntity) -> None:
        """Update an existing booking."""
        ...

    @abstractmethod
    def soft_delete(self, booking_id: int) -> bool:
        """Soft-delete a booking. Returns True if found."""
        ...
