"""
Booking domain entity — DDD for amenity reservations.

A booking links an amenity to a unit+owner with fee and security deposit tracking.
"""
from datetime import datetime, date
from decimal import Decimal
from typing import Optional, Dict, Any


class BookingEntity:
    """Entidad de dominio para reservas de amenidades."""

    VALID_STATUSES = {'draft', 'pending_approval', 'confirmed', 'cancelled', 'completed'}
    VALID_DEPOSIT_STATUSES = {
        'not_required', 'pending', 'paid', 'returned',
        'partially_applied', 'applied', 'forfeited',
    }

    def __init__(
        self,
        id: int,
        uuid: str,
        condominium_id: int,
        building_id: int,
        amenity_id: int,
        unit_id: int,
        owner_id: int,
        unit_number_snapshot: Optional[str] = None,
        owner_name_snapshot: Optional[str] = None,
        booking_date: Optional[date] = None,
        start_at: Optional[datetime] = None,
        end_at: Optional[datetime] = None,
        status: str = 'draft',
        booking_fee_amount: Decimal = Decimal('0.00'),
        security_deposit_amount: Decimal = Decimal('0.00'),
        currency: str = 'PEN',
        booking_fee_ar_id: Optional[int] = None,
        security_deposit_ar_id: Optional[int] = None,
        deposit_status: str = 'not_required',
        notes: Optional[str] = None,
        created_by: Optional[int] = None,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None,
        deleted_at: Optional[datetime] = None,
        # Enriched
        amenity_name: Optional[str] = None,
        unit_code: Optional[str] = None,
        owner_name: Optional[str] = None,
        building_name: Optional[str] = None,
    ) -> None:
        self.id = id
        self.uuid = uuid
        self.condominium_id = condominium_id
        self.building_id = building_id
        self.amenity_id = amenity_id
        self.unit_id = unit_id
        self.owner_id = owner_id
        self.unit_number_snapshot = unit_number_snapshot
        self.owner_name_snapshot = owner_name_snapshot
        self.booking_date = booking_date
        self.start_at = start_at
        self.end_at = end_at
        self.status = status
        self.booking_fee_amount = booking_fee_amount
        self.security_deposit_amount = security_deposit_amount
        self.currency = currency
        self.booking_fee_ar_id = booking_fee_ar_id
        self.security_deposit_ar_id = security_deposit_ar_id
        self.deposit_status = deposit_status
        self.notes = notes
        self.created_by = created_by
        self.created_at = created_at
        self.updated_at = updated_at
        self.deleted_at = deleted_at
        # Enrichment
        self.amenity_name = amenity_name
        self.unit_code = unit_code
        self.owner_name = owner_name
        self.building_name = building_name

    # ── computed properties ──

    @property
    def has_booking_fee(self) -> bool:
        return self.booking_fee_amount > 0

    @property
    def has_security_deposit(self) -> bool:
        return self.security_deposit_amount > 0

    @property
    def total_to_collect(self) -> Decimal:
        return self.booking_fee_amount + self.security_deposit_amount

    @property
    def fee_is_paid(self) -> bool:
        return self.booking_fee_ar_id is not None

    @property
    def deposit_is_paid(self) -> bool:
        return self.deposit_status in ('paid', 'returned', 'partially_applied', 'applied')

    @property
    def is_active(self) -> bool:
        return self.status in ('draft', 'pending_approval', 'confirmed')

    def can_transition_to(self, new_status: str) -> bool:
        transitions = {
            'draft': ('pending_approval', 'confirmed', 'cancelled'),
            'pending_approval': ('confirmed', 'cancelled'),
            'confirmed': ('completed', 'cancelled'),
            'cancelled': (),
            'completed': (),
        }
        return new_status in transitions.get(self.status, ())

    def to_dict(self) -> Dict[str, Any]:
        return {
            'id': self.id,
            'uuid': self.uuid,
            'condominium_id': self.condominium_id,
            'building_id': self.building_id,
            'amenity_id': self.amenity_id,
            'unit_id': self.unit_id,
            'owner_id': self.owner_id,
            'unit_number_snapshot': self.unit_number_snapshot,
            'owner_name_snapshot': self.owner_name_snapshot,
            'booking_date': self.booking_date.isoformat() if self.booking_date else None,
            'start_at': self.start_at.isoformat() if self.start_at else None,
            'end_at': self.end_at.isoformat() if self.end_at else None,
            'status': self.status,
            'booking_fee_amount': float(self.booking_fee_amount),
            'security_deposit_amount': float(self.security_deposit_amount),
            'currency': self.currency,
            'booking_fee_ar_id': self.booking_fee_ar_id,
            'security_deposit_ar_id': self.security_deposit_ar_id,
            'deposit_status': self.deposit_status,
            'notes': self.notes,
            'created_by': self.created_by,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            # Enriched
            'amenity_name': self.amenity_name,
            'unit_code': self.unit_code,
            'owner_name': self.owner_name,
            'building_name': self.building_name,
            # Computed
            'has_booking_fee': self.has_booking_fee,
            'has_security_deposit': self.has_security_deposit,
            'total_to_collect': float(self.total_to_collect),
            'fee_is_paid': self.fee_is_paid,
            'deposit_is_paid': self.deposit_is_paid,
        }
