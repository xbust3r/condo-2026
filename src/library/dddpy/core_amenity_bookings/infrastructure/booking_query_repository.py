"""
Booking query repository — SQLAlchemy implementation.
"""
from datetime import datetime
from typing import Optional, List, Tuple

from sqlalchemy import and_, or_

from library.dddpy.shared.mysql.session_manager import session_scope
from library.dddpy.core_amenity_bookings.domain.booking_entity import BookingEntity
from library.dddpy.core_amenity_bookings.domain.booking_query_repository import BookingQueryRepository
from library.dddpy.core_amenity_bookings.infrastructure.dbbooking import DBBooking
from library.dddpy.core_amenity_bookings.infrastructure.booking_mapper import BookingMapper


class BookingQueryRepositoryImpl(BookingQueryRepository):

    def get_by_id(self, booking_id: int) -> Optional[BookingEntity]:
        with session_scope() as session:
            db_row = session.query(DBBooking).filter(
                DBBooking.id == booking_id,
                DBBooking.deleted_at.is_(None),
            ).first()
            return BookingMapper.to_domain(db_row) if db_row else None

    def get_by_uuid(self, uuid: str) -> Optional[BookingEntity]:
        with session_scope() as session:
            db_row = session.query(DBBooking).filter(
                DBBooking.uuid == uuid,
                DBBooking.deleted_at.is_(None),
            ).first()
            return BookingMapper.to_domain(db_row) if db_row else None

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
        with session_scope() as session:
            query = session.query(DBBooking)

            if not include_deleted:
                query = query.filter(DBBooking.deleted_at.is_(None))
            if condominium_id is not None:
                query = query.filter(DBBooking.condominium_id == condominium_id)
            if building_id is not None:
                query = query.filter(DBBooking.building_id == building_id)
            if amenity_id is not None:
                query = query.filter(DBBooking.amenity_id == amenity_id)
            if unit_id is not None:
                query = query.filter(DBBooking.unit_id == unit_id)
            if owner_id is not None:
                query = query.filter(DBBooking.owner_id == owner_id)
            if status is not None:
                query = query.filter(DBBooking.status == status)

            total = query.count()
            rows = query.order_by(DBBooking.start_at.desc()).offset(skip).limit(limit).all()

            entities = [BookingMapper.to_domain(row) for row in rows]
            return entities, total

    def find_overlapping(
        self,
        amenity_id: int,
        start_at,
        end_at,
        exclude_booking_id: Optional[int] = None,
    ) -> List[BookingEntity]:
        """Find bookings that overlap: existing.start < new.end AND existing.end > new.start"""
        with session_scope() as session:
            query = session.query(DBBooking).filter(
                DBBooking.amenity_id == amenity_id,
                DBBooking.deleted_at.is_(None),
                DBBooking.status.in_(['confirmed', 'pending_approval']),
                DBBooking.start_at < end_at,
                DBBooking.end_at > start_at,
            )
            if exclude_booking_id is not None:
                query = query.filter(DBBooking.id != exclude_booking_id)

            rows = query.all()
            return [BookingMapper.to_domain(row) for row in rows]
