"""
Booking Use Case — business logic for amenity reservations.

Handles:
- Booking CRUD with validation (unit→owner→building, overlap detection)
- Confirmation: generates AR entries for booking_fee + security_deposit
- Cancellation with AR cleanup
- Deposit lifecycle (return/partial_apply/full_apply)
"""
import uuid as uuid_lib
from datetime import datetime, date
from decimal import Decimal
from typing import Optional

from library.dddpy.core_amenity_bookings.domain.booking_entity import BookingEntity
from library.dddpy.core_amenity_bookings.domain.booking_exception import (
    BookingNotFound,
    BookingValidationError,
    BookingOverlapError,
    BookingStatusError,
)
from library.dddpy.core_amenity_bookings.domain.booking_cmd_repository import BookingCmdRepository
from library.dddpy.core_amenity_bookings.domain.booking_query_repository import BookingQueryRepository
from library.dddpy.core_amenity_bookings.infrastructure.booking_cmd_repository import BookingCmdRepositoryImpl
from library.dddpy.core_amenity_bookings.infrastructure.booking_query_repository import BookingQueryRepositoryImpl
from library.dddpy.shared.logging.logging import Logger
from library.dddpy.shared.schemas.response_schema import ResponseSuccessSchema
from library.dddpy.shared.mysql.session_manager import session_scope


logger = Logger("BookingUseCase")


class BookingUseCase:

    def __init__(self):
        self._cmd_repo = BookingCmdRepositoryImpl()
        self._query_repo = BookingQueryRepositoryImpl()

    # ── Validation helpers ───────────────────────────────────────────

    def _get_amenity(self, amenity_id: int):
        """Fetch amenity with its pricing/deposit config."""
        from library.dddpy.core_amenities.infrastructure.dbamenity import DBAmenity
        with session_scope() as session:
            amenity = session.query(DBAmenity).filter(
                DBAmenity.id == amenity_id,
                DBAmenity.deleted_at.is_(None),
            ).first()
            if not amenity:
                raise BookingValidationError(f"Amenity id={amenity_id} not found")
            return amenity

    def _validate_unit_belongs_to_building(self, unit_id: int, building_id: int):
        from library.dddpy.core_buildings.infrastructure.dbbuildings import DBBuildings
        with session_scope() as session:
            from library.dddpy.shared.mysql.base import Base
            # core_units belongs to core_buildings
            result = session.execute(
                session.query(DBBuildings.id).filter(
                    DBBuildings.id == building_id,
                    DBBuildings.deleted_at.is_(None),
                ).exists()
            )
            # Check unit → building relationship via core_buildings
            from sqlalchemy import text
            row = session.execute(
                text("""
                    SELECT 1 FROM core_units u
                    JOIN core_buildings b ON b.id = :building_id
                    WHERE u.id = :unit_id
                    AND u.building_id = b.id
                    AND u.deleted_at IS NULL
                    AND b.deleted_at IS NULL
                """),
                {"unit_id": unit_id, "building_id": building_id},
            ).first()
            if not row:
                raise BookingValidationError(
                    f"Unit id={unit_id} does not belong to building id={building_id}"
                )

    def _validate_owner_belongs_to_unit(self, unit_id: int, owner_id: int):
        """Check that owner_id is linked to the unit via ownership."""
        from sqlalchemy import text
        with session_scope() as session:
            row = session.execute(
                text("""
                    SELECT 1 FROM core_unit_ownerships
                    WHERE unit_id = :unit_id
                    AND owner_user_id = :owner_id
                    AND deleted_at IS NULL
                """),
                {"unit_id": unit_id, "owner_id": owner_id},
            ).first()
            if not row:
                raise BookingValidationError(
                    f"Owner id={owner_id} does not own unit id={unit_id}"
                )

    def _get_unit_and_owner_snapshots(self, unit_id: int, owner_id: int):
        """Capture unit number and owner name for audit trail."""
        from sqlalchemy import text
        with session_scope() as session:
            result = session.execute(
                text("""
                    SELECT u.code AS unit_code, u2.display_name AS owner_name
                    FROM core_units u
                    JOIN users u2 ON u2.id = :owner_id
                    WHERE u.id = :unit_id AND u.deleted_at IS NULL
                """),
                {"unit_id": unit_id, "owner_id": owner_id},
            ).first()
            if result:
                return result.unit_code, result.owner_name
            return None, None

    def _check_overlap(self, amenity_id: int, start_at, end_at, exclude_id: Optional[int] = None):
        overlapping = self._query_repo.find_overlapping(
            amenity_id=amenity_id,
            start_at=start_at,
            end_at=end_at,
            exclude_booking_id=exclude_id,
        )
        if overlapping:
            raise BookingOverlapError(
                f"Amenity id={amenity_id} already has {len(overlapping)} "
                f"booking(s) in the requested time range"
            )

    def _generate_ar(
        self,
        condominium_id: int,
        unit_id: int,
        debtor_user_id: int,
        amount: Decimal,
        description: str,
        origin_type: str,
        origin_id: int,
        due_date: date,
        period: Optional[str] = None,
    ) -> int:
        """Generate an AR entry and return its id."""
        import uuid as ar_uuid
        from library.dddpy.core_accounts_receivable.infrastructure.dbar import DBAR

        with session_scope() as session:
            db_ar = DBAR(
                uuid=str(ar_uuid.uuid4()),
                condominium_id=condominium_id,
                unit_id=unit_id,
                debtor_user_id=debtor_user_id,
                reference_code=f"BOOK-{origin_id}",
                description=description,
                amount=amount,
                paid_amount=Decimal('0.00'),
                currency='PEN',
                status='pending',
                due_date=due_date,
                period=period,
                charge_id=None,
                origin_type=origin_type,
                origin_id=origin_id,
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow(),
            )
            session.add(db_ar)
            session.flush()
            return db_ar.id

    # ── CRUD ──────────────────────────────────────────────────────────

    def create(
        self,
        condominium_id: int,
        building_id: int,
        amenity_id: int,
        unit_id: int,
        owner_id: int,
        booking_date: date,
        start_at: datetime,
        end_at: datetime,
        notes: Optional[str] = None,
        created_by: Optional[int] = None,
    ) -> ResponseSuccessSchema:
        logger.add_inside_method("create")

        # Validate amenity exists and is reservable
        amenity = self._get_amenity(amenity_id)
        if not amenity.is_reservable:
            raise BookingValidationError(f"Amenity id={amenity_id} is not reservable")

        # Validate unit → building
        self._validate_unit_belongs_to_building(unit_id, building_id)

        # Validate owner → unit
        self._validate_owner_belongs_to_unit(unit_id, owner_id)

        # Validate no overlap
        self._check_overlap(amenity_id, start_at, end_at)

        # Capture snapshots
        unit_code, owner_name = self._get_unit_and_owner_snapshots(unit_id, owner_id)

        # Determine initial status
        initial_status = 'pending_approval' if amenity.requires_approval else 'draft'

        # Determine deposit status
        deposit_status = 'not_required'
        if float(amenity.security_deposit_amount or 0) > 0:
            deposit_status = 'pending'

        entity = BookingEntity(
            id=0,
            uuid=str(uuid_lib.uuid4()),
            condominium_id=condominium_id,
            building_id=building_id,
            amenity_id=amenity_id,
            unit_id=unit_id,
            owner_id=owner_id,
            unit_number_snapshot=unit_code,
            owner_name_snapshot=owner_name,
            booking_date=booking_date,
            start_at=start_at,
            end_at=end_at,
            status=initial_status,
            booking_fee_amount=amenity.booking_price or Decimal('0.00'),
            security_deposit_amount=amenity.security_deposit_amount or Decimal('0.00'),
            currency='PEN',
            deposit_status=deposit_status,
            notes=notes,
            created_by=created_by,
            created_at=datetime.utcnow(),
        )

        booking_id = self._cmd_repo.create(entity)
        entity.id = booking_id
        logger.info(f"Booking created id={booking_id} amenity={amenity_id} unit={unit_id}")

        return ResponseSuccessSchema(
            success=True,
            message="Booking created",
            data=entity.to_dict(),
        )

    def get_by_id(self, id: int) -> ResponseSuccessSchema:
        entity = self._query_repo.get_by_id(id)
        if not entity:
            raise BookingNotFound()
        return ResponseSuccessSchema(
            success=True,
            message="Booking found",
            data=entity.to_dict(),
        )

    def get_by_uuid(self, uuid: str) -> ResponseSuccessSchema:
        entity = self._query_repo.get_by_uuid(uuid)
        if not entity:
            raise BookingNotFound()
        return ResponseSuccessSchema(
            success=True,
            message="Booking found",
            data=entity.to_dict(),
        )

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
    ) -> ResponseSuccessSchema:
        entities, total = self._query_repo.list_all(
            condominium_id=condominium_id,
            building_id=building_id,
            amenity_id=amenity_id,
            unit_id=unit_id,
            owner_id=owner_id,
            status=status,
            skip=skip,
            limit=limit,
            include_deleted=include_deleted,
        )
        return ResponseSuccessSchema(
            success=True,
            message="Bookings retrieved",
            data=[e.to_dict() for e in entities],
            total=total,
            skip=skip,
            limit=limit,
        )

    def update(self, id: int, request) -> ResponseSuccessSchema:
        existing = self._query_repo.get_by_id(id)
        if not existing:
            raise BookingNotFound()
        if existing.status not in ('draft', 'pending_approval'):
            raise BookingStatusError(
                f"Cannot update booking in status '{existing.status}'"
            )

        new_start = request.start_at if request.start_at is not None else existing.start_at
        new_end = request.end_at if request.end_at is not None else existing.end_at
        if new_start >= new_end:
            raise BookingValidationError("start_at must be before end_at")

        # Check overlap (excluding self)
        self._check_overlap(existing.amenity_id, new_start, new_end, exclude_id=id)

        entity = BookingEntity(
            id=existing.id,
            uuid=existing.uuid,
            condominium_id=existing.condominium_id,
            building_id=existing.building_id,
            amenity_id=existing.amenity_id,
            unit_id=existing.unit_id,
            owner_id=existing.owner_id,
            unit_number_snapshot=existing.unit_number_snapshot,
            owner_name_snapshot=existing.owner_name_snapshot,
            booking_date=existing.booking_date,
            start_at=new_start,
            end_at=new_end,
            status=existing.status,
            booking_fee_amount=existing.booking_fee_amount,
            security_deposit_amount=existing.security_deposit_amount,
            currency=existing.currency,
            booking_fee_ar_id=existing.booking_fee_ar_id,
            security_deposit_ar_id=existing.security_deposit_ar_id,
            deposit_status=existing.deposit_status,
            notes=request.notes if request.notes is not None else existing.notes,
            created_by=existing.created_by,
            created_at=existing.created_at,
            updated_at=datetime.utcnow(),
        )
        self._cmd_repo.update(entity)
        updated = self._query_repo.get_by_id(id)

        return ResponseSuccessSchema(
            success=True,
            message="Booking updated",
            data=updated.to_dict(),
        )

    def soft_delete(self, id: int) -> ResponseSuccessSchema:
        ok = self._cmd_repo.soft_delete(id)
        if not ok:
            raise BookingNotFound()
        return ResponseSuccessSchema(success=True, message="Booking cancelled", data=None)

    # ── Lifecycle ─────────────────────────────────────────────────────

    def confirm(self, id: int) -> ResponseSuccessSchema:
        """Confirm booking → generates AR entries for fee and deposit."""
        logger.add_inside_method("confirm")
        existing = self._query_repo.get_by_id(id)
        if not existing:
            raise BookingNotFound()
        if existing.status not in ('draft', 'pending_approval'):
            raise BookingStatusError(
                f"Cannot confirm booking in status '{existing.status}'"
            )

        now = datetime.utcnow()
        period = existing.booking_date.strftime('%Y-%m') if existing.booking_date else None
        due_date = existing.booking_date if existing.booking_date else date.today()

        # Generate AR for booking fee
        if existing.has_booking_fee:
            fee_ar_id = self._generate_ar(
                condominium_id=existing.condominium_id,
                unit_id=existing.unit_id,
                debtor_user_id=existing.owner_id,
                amount=existing.booking_fee_amount,
                description=f"Reserva: {existing.amenity_name or 'amenity'} — Fee",
                origin_type='amenity_booking_fee',
                origin_id=existing.id,
                due_date=due_date,
                period=period,
            )
            existing.booking_fee_ar_id = fee_ar_id
            logger.info(f"AR fee generated id={fee_ar_id} for booking={existing.id}")

        # Generate AR for security deposit
        if existing.has_security_deposit:
            deposit_ar_id = self._generate_ar(
                condominium_id=existing.condominium_id,
                unit_id=existing.unit_id,
                debtor_user_id=existing.owner_id,
                amount=existing.security_deposit_amount,
                description=f"Reserva: {existing.amenity_name or 'amenity'} — Garantía",
                origin_type='amenity_security_deposit',
                origin_id=existing.id,
                due_date=due_date,
                period=period,
            )
            existing.security_deposit_ar_id = deposit_ar_id
            existing.deposit_status = 'pending'
            logger.info(f"AR deposit generated id={deposit_ar_id} for booking={existing.id}")

        existing.status = 'confirmed'
        existing.updated_at = now
        self._cmd_repo.update(existing)

        updated = self._query_repo.get_by_id(id)
        return ResponseSuccessSchema(
            success=True,
            message="Booking confirmed — AR entries generated",
            data=updated.to_dict(),
        )

    def cancel(self, id: int, reason: Optional[str] = None) -> ResponseSuccessSchema:
        """Cancel booking. If ARs exist, they remain (manual handling via deposit flow)."""
        logger.add_inside_method("cancel")
        existing = self._query_repo.get_by_id(id)
        if not existing:
            raise BookingNotFound()
        if existing.status in ('cancelled', 'completed'):
            raise BookingStatusError(
                f"Cannot cancel booking in status '{existing.status}'"
            )

        existing.status = 'cancelled'
        existing.notes = (existing.notes or '') + (f"\nCancel reason: {reason}" if reason else '')
        existing.updated_at = datetime.utcnow()
        self._cmd_repo.update(existing)

        updated = self._query_repo.get_by_id(id)
        return ResponseSuccessSchema(
            success=True,
            message="Booking cancelled",
            data=updated.to_dict(),
        )

    def complete(self, id: int) -> ResponseSuccessSchema:
        """Mark booking as completed after use."""
        existing = self._query_repo.get_by_id(id)
        if not existing:
            raise BookingNotFound()
        if existing.status != 'confirmed':
            raise BookingStatusError(
                f"Cannot complete booking in status '{existing.status}'"
            )

        existing.status = 'completed'
        existing.updated_at = datetime.utcnow()
        self._cmd_repo.update(existing)

        updated = self._query_repo.get_by_id(id)
        return ResponseSuccessSchema(
            success=True,
            message="Booking completed",
            data=updated.to_dict(),
        )

    # ── Deposit lifecycle ─────────────────────────────────────────────

    def _record_deposit_movement(
        self,
        booking_id: int,
        movement_type: str,
        amount: Decimal,
        notes: Optional[str] = None,
        created_by: Optional[int] = None,
    ) -> None:
        """Insert a deposit movement record."""
        import uuid as muuid
        from sqlalchemy import text
        with session_scope() as session:
            session.execute(
                text("""
                    INSERT INTO core_amenity_deposit_movements
                    (uuid, booking_id, movement_type, amount, currency, notes, created_by, created_at)
                    VALUES (:uuid, :booking_id, :movement_type, :amount, 'PEN', :notes, :created_by, NOW())
                """),
                {
                    "uuid": str(muuid.uuid4()),
                    "booking_id": booking_id,
                    "movement_type": movement_type,
                    "amount": float(amount),
                    "notes": notes,
                    "created_by": created_by,
                },
            )
            session.flush()

    def return_deposit(self, id: int, notes: Optional[str] = None) -> ResponseSuccessSchema:
        """Full refund of security deposit."""
        existing = self._query_repo.get_by_id(id)
        if not existing:
            raise BookingNotFound()
        if existing.deposit_status not in ('paid',):
            raise BookingStatusError(
                f"Cannot return deposit in status '{existing.deposit_status}'. Must be 'paid'."
            )
        if not existing.has_security_deposit:
            raise BookingValidationError("This booking has no security deposit")

        self._record_deposit_movement(
            booking_id=id,
            movement_type='return',
            amount=existing.security_deposit_amount,
            notes=notes,
        )

        existing.deposit_status = 'returned'
        existing.updated_at = datetime.utcnow()
        self._cmd_repo.update(existing)

        updated = self._query_repo.get_by_id(id)
        return ResponseSuccessSchema(
            success=True,
            message="Deposit fully returned",
            data=updated.to_dict(),
        )

    def apply_deposit(
        self,
        id: int,
        action: str,
        amount: float,
        notes: Optional[str] = None,
    ) -> ResponseSuccessSchema:
        """Partial or full application of deposit for damages."""
        existing = self._query_repo.get_by_id(id)
        if not existing:
            raise BookingNotFound()
        if existing.deposit_status not in ('paid', 'partially_applied'):
            raise BookingStatusError(
                f"Cannot apply deposit in status '{existing.deposit_status}'. Must be 'paid' or 'partially_applied'."
            )
        if not existing.has_security_deposit:
            raise BookingValidationError("This booking has no security deposit")

        amount_dec = Decimal(str(amount))
        if amount_dec <= 0:
            raise BookingValidationError("Amount must be > 0")

        remaining = existing.security_deposit_amount
        if existing.deposit_status == 'partially_applied':
            # Calculate remaining by summing past movements
            from sqlalchemy import text
            with session_scope() as session:
                charged = session.execute(
                    text("""
                        SELECT COALESCE(SUM(amount), 0) FROM core_amenity_deposit_movements
                        WHERE booking_id = :bid AND movement_type = 'charge'
                    """),
                    {"bid": id},
                ).scalar() or 0
                returned = session.execute(
                    text("""
                        SELECT COALESCE(SUM(amount), 0) FROM core_amenity_deposit_movements
                        WHERE booking_id = :bid AND movement_type IN ('return', 'partial_apply', 'full_apply')
                    """),
                    {"bid": id},
                ).scalar() or 0
                remaining = existing.security_deposit_amount - Decimal(str(returned))

        if amount_dec > remaining:
            raise BookingValidationError(
                f"Amount {amount} exceeds remaining deposit {float(remaining)}"
            )

        movement_type = 'full_apply' if amount_dec >= remaining else 'partial_apply'
        new_deposit_status = 'applied' if movement_type == 'full_apply' else 'partially_applied'

        self._record_deposit_movement(
            booking_id=id,
            movement_type=movement_type,
            amount=amount_dec,
            notes=notes,
        )

        existing.deposit_status = new_deposit_status
        existing.updated_at = datetime.utcnow()
        self._cmd_repo.update(existing)

        updated = self._query_repo.get_by_id(id)
        return ResponseSuccessSchema(
            success=True,
            message=f"Deposit {movement_type} — {amount} applied",
            data=updated.to_dict(),
        )
