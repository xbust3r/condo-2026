"""
Booking mapper — maps between DB model and domain entity.
"""
from typing import Optional
from decimal import Decimal

from library.dddpy.core_amenity_bookings.infrastructure.dbbooking import DBBooking
from library.dddpy.core_amenity_bookings.domain.booking_entity import BookingEntity


class BookingMapper:

    @staticmethod
    def to_domain(db_row: DBBooking) -> BookingEntity:
        return BookingEntity(
            id=db_row.id,
            uuid=db_row.uuid,
            condominium_id=db_row.condominium_id,
            building_id=db_row.building_id,
            amenity_id=db_row.amenity_id,
            unit_id=db_row.unit_id,
            owner_id=db_row.owner_id,
            unit_number_snapshot=db_row.unit_number_snapshot,
            owner_name_snapshot=db_row.owner_name_snapshot,
            booking_date=db_row.booking_date,
            start_at=db_row.start_at,
            end_at=db_row.end_at,
            status=db_row.status or 'draft',
            booking_fee_amount=db_row.booking_fee_amount or Decimal('0.00'),
            security_deposit_amount=db_row.security_deposit_amount or Decimal('0.00'),
            currency=db_row.currency or 'PEN',
            booking_fee_ar_id=db_row.booking_fee_ar_id,
            security_deposit_ar_id=db_row.security_deposit_ar_id,
            deposit_status=db_row.deposit_status or 'not_required',
            notes=db_row.notes,
            created_by=db_row.created_by,
            created_at=db_row.created_at,
            updated_at=db_row.updated_at,
            deleted_at=db_row.deleted_at,
            guest_count=db_row.guest_count or 1,
            allocation_source=db_row.allocation_source or 'DIRECT',
            waitlist_entry_id=db_row.waitlist_entry_id,
            idempotency_key=db_row.idempotency_key,
            policy_snapshot_json=db_row.policy_snapshot_json,
            allocation_reason_json=db_row.allocation_reason_json,
        )

    @staticmethod
    def to_domain_enriched(
        db_row: DBBooking,
        amenity_name: Optional[str] = None,
        unit_code: Optional[str] = None,
        owner_name: Optional[str] = None,
        building_name: Optional[str] = None,
    ) -> BookingEntity:
        entity = BookingMapper.to_domain(db_row)
        entity.amenity_name = amenity_name
        entity.unit_code = unit_code
        entity.owner_name = owner_name
        entity.building_name = building_name
        return entity
