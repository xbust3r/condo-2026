"""
Booking command repository — SQLAlchemy implementation.
"""
from datetime import datetime
from library.dddpy.shared.mysql.session_manager import session_scope
from library.dddpy.core_amenity_bookings.domain.booking_entity import BookingEntity
from library.dddpy.core_amenity_bookings.domain.booking_cmd_repository import BookingCmdRepository
from library.dddpy.core_amenity_bookings.infrastructure.dbbooking import DBBooking
from library.dddpy.core_amenity_bookings.infrastructure.booking_mapper import BookingMapper


class BookingCmdRepositoryImpl(BookingCmdRepository):

    def create(self, entity: BookingEntity) -> int:
        with session_scope() as session:
            db_booking = DBBooking(
                uuid=entity.uuid,
                condominium_id=entity.condominium_id,
                building_id=entity.building_id,
                amenity_id=entity.amenity_id,
                unit_id=entity.unit_id,
                owner_id=entity.owner_id,
                unit_number_snapshot=entity.unit_number_snapshot,
                owner_name_snapshot=entity.owner_name_snapshot,
                booking_date=entity.booking_date,
                start_at=entity.start_at,
                end_at=entity.end_at,
                status=entity.status,
                booking_fee_amount=entity.booking_fee_amount,
                security_deposit_amount=entity.security_deposit_amount,
                currency=entity.currency,
                booking_fee_ar_id=entity.booking_fee_ar_id,
                security_deposit_ar_id=entity.security_deposit_ar_id,
                deposit_status=entity.deposit_status,
                notes=entity.notes,
                created_by=entity.created_by,
                created_at=entity.created_at or datetime.utcnow(),
                updated_at=datetime.utcnow(),
            )
            session.add(db_booking)
            session.flush()
            return db_booking.id

    def update(self, entity: BookingEntity) -> None:
        with session_scope() as session:
            db_booking = session.query(DBBooking).filter(
                DBBooking.id == entity.id,
                DBBooking.deleted_at.is_(None),
            ).first()
            if not db_booking:
                return
            db_booking.status = entity.status
            db_booking.booking_fee_amount = entity.booking_fee_amount
            db_booking.security_deposit_amount = entity.security_deposit_amount
            db_booking.booking_fee_ar_id = entity.booking_fee_ar_id
            db_booking.security_deposit_ar_id = entity.security_deposit_ar_id
            db_booking.deposit_status = entity.deposit_status
            db_booking.notes = entity.notes
            db_booking.start_at = entity.start_at
            db_booking.end_at = entity.end_at
            db_booking.updated_at = datetime.utcnow()
            session.flush()

    def soft_delete(self, booking_id: int) -> bool:
        with session_scope() as session:
            db_booking = session.query(DBBooking).filter(
                DBBooking.id == booking_id,
                DBBooking.deleted_at.is_(None),
            ).first()
            if not db_booking:
                return False
            db_booking.deleted_at = datetime.utcnow()
            db_booking.status = 'cancelled'
            session.flush()
            return True
