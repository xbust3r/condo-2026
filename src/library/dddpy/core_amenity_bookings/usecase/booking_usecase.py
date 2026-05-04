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
from typing import Optional, Any

from sqlalchemy import text

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
        self._lock_session = None  # held during named-lock scope (B5)

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
            # Load lazy attributes before session is closed by session_scope()
            _ = (
                amenity.is_reservable,
                amenity.requires_approval,
                amenity.booking_price,
                amenity.security_deposit_amount,
            )
            session.expunge(amenity)
            return amenity

    def _validate_unit_belongs_to_building(self, unit_id: int, building_id: int):
        with session_scope() as session:
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
                    AND user_id = :owner_id
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
                    SELECT u.code AS unit_code,
                           CONCAT(COALESCE(up.first_name, ''),
                                  IF(up.last_name IS NOT NULL, CONCAT(' ', up.last_name), ''),
                                  IF(up.first_name IS NULL AND up.last_name IS NULL, u2.email, '')
                           ) AS owner_name
                    FROM core_units u
                    JOIN users u2 ON u2.id = :owner_id
                    LEFT JOIN user_profiles up ON up.user_id = u2.id
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

    def _check_unit_overlap(
        self, amenity_id: int, unit_id: int, start_at, end_at,
        exclude_id: Optional[int] = None,
    ):
        """Check that the same unit doesn't double-book the same time slot."""
        from sqlalchemy import text
        with session_scope() as session:
            params = {
                'amenity_id': amenity_id,
                'unit_id': unit_id,
                'start_at': start_at,
                'end_at': end_at,
            }
            exclude = ''
            if exclude_id is not None:
                exclude = ' AND b.id != :exclude_id'
                params['exclude_id'] = exclude_id
            row = session.execute(
                text(f"""
                    SELECT COUNT(*) FROM core_amenity_bookings b
                    WHERE b.amenity_id = :amenity_id
                      AND b.unit_id = :unit_id
                      AND b.status IN ('draft', 'pending_approval', 'confirmed')
                      AND b.deleted_at IS NULL
                      AND b.start_at < :end_at
                      AND b.end_at > :start_at
                      {exclude}
                """),
                params,
            ).fetchone()
            if row and row[0] > 0:
                raise BookingOverlapError(
                    f"Unit id={unit_id} already has {row[0]} booking(s) "
                    f"for amenity id={amenity_id} in this time range"
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
        guest_count: int = 1,
        idempotency_key: Optional[str] = None,
        allocation_source: str = 'DIRECT',
    ) -> ResponseSuccessSchema:
        logger.add_inside_method("create")

        # ── Phase 0: Idempotency check — if key was already used, return existing (B5)
        # Must run before any validation or lock: retries are safe by definition
        if idempotency_key:
            existing = self._query_repo.find_by_idempotency_key(
                condominium_id, idempotency_key
            )
            if existing:
                return ResponseSuccessSchema(
                    success=True,
                    message='Booking already exists (idempotent retry)',
                    data=existing.to_dict(),
                )

        # ── Phase 1: Basic integrity ─────────────────────────────────
        amenity = self._get_amenity(amenity_id)
        if not amenity.is_reservable:
            raise BookingValidationError(f"Amenity id={amenity_id} is not reservable")

        self._validate_unit_belongs_to_building(unit_id, building_id)
        self._validate_owner_belongs_to_unit(unit_id, owner_id)

        # ── Acquire per-amenity lock to serialize concurrent bookings (B5) ──
        # MySQL named lock: blocks other sessions trying to book the same amenity
        # timeout=10s prevents indefinite deadlock; different amenities don't contend
        lock_name = f'booking_amenity_{amenity_id}'
        self._acquire_amenity_lock(lock_name)
        try:
            result = self._create_locked(
                condominium_id=condominium_id,
                building_id=building_id,
                amenity_id=amenity_id,
                unit_id=unit_id,
                owner_id=owner_id,
                booking_date=booking_date,
                start_at=start_at,
                end_at=end_at,
                notes=notes,
                created_by=created_by,
                guest_count=guest_count,
                idempotency_key=idempotency_key,
                amenity=amenity,
                allocation_source=allocation_source,
            )
        except (BookingValidationError, BookingOverlapError) as e:
            # B7: Allocation audit — booking rejected
            from library.dddpy.core_amenity_bookings.usecase.allocation_audit_usecase import AllocationAuditUseCase
            try:
                AllocationAuditUseCase().record(
                    amenity_id=amenity_id,
                    decision_type='BOOKING_REJECTED',
                    decision_reason=str(e)[:255],
                    context={
                        'unit_id': unit_id,
                        'owner_id': owner_id,
                        'booking_date': booking_date.isoformat() if booking_date else None,
                        'guest_count': guest_count,
                    },
                )
            except Exception:
                pass  # Audit failure must not block the rejection
            raise
        finally:
            self._release_amenity_lock(lock_name)

        return result

    def _acquire_amenity_lock(self, lock_name: str) -> None:
        """Acquire MySQL named lock with 10s timeout."""
        self._lock_session = session_scope().__enter__()
        row = self._lock_session.execute(
            text("SELECT GET_LOCK(:name, 10) AS acquired"),
            {'name': lock_name},
        ).fetchone()
        if not row or not row[0]:
            self._lock_session.__exit__(None, None, None)
            self._lock_session = None
            raise BookingValidationError(
                f"Could not acquire lock for amenity — try again later."
            )

    def _release_amenity_lock(self, lock_name: str) -> None:
        """Release MySQL named lock."""
        try:
            self._lock_session.execute(
                text("SELECT RELEASE_LOCK(:name)"),
                {'name': lock_name},
            )
        finally:
            self._lock_session.__exit__(None, None, None)
            self._lock_session = None

    def _create_locked(
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
        guest_count: int = 1,
        idempotency_key: Optional[str] = None,
        amenity: Any = None,
        allocation_source: str = 'DIRECT',
    ) -> ResponseSuccessSchema:
        logger.add_inside_method("_create_locked")

        # ── Phase 2: Policy resolution + validation (B2-B4) ──────────
        from library.dddpy.core_amenity_bookings.usecase.policy_resolver import get_policy_resolver
        from library.dddpy.core_amenity_bookings.usecase.booking_policy_validator import BookingPolicyValidator

        resolver = get_policy_resolver()
        policy = resolver.resolve(condominium_id, amenity_id)
        amenity_type = resolver._lookup_amenity_type(amenity_id)
        validator = BookingPolicyValidator()

        # Overlap check: depends on slot_mode from policy
        #   DISCRETE_WINDOWS → strict: no two bookings at same time
        #   CONTINUOUS_SLOTS → capacity handles concurrency; only block same-unit overlap
        try:
            if policy.slot_mode == 'DISCRETE_WINDOWS':
                self._check_overlap(amenity_id, start_at, end_at)
            else:
                self._check_unit_overlap(amenity_id, unit_id, start_at, end_at)
        except BookingOverlapError as overlap_err:
            # B6: DISCRETE_WINDOWS overlap = slot full → route to waitlist
            if policy.waitlist_mode and policy.waitlist_mode not in ('none', 'disabled'):
                from library.dddpy.core_amenity_bookings.usecase.waitlist_usecase import WaitlistUseCase
                wl_uc = WaitlistUseCase()
                wl_snapshot = validator.build_policy_snapshot(policy)
                wl_id = wl_uc.create_entry(
                    amenity_id=amenity_id,
                    unit_id=unit_id,
                    user_id=owner_id,
                    booking_date=booking_date,
                    requested_start_at=start_at,
                    requested_end_at=end_at,
                    guest_count=guest_count,
                    idempotency_key=idempotency_key,
                    policy_snapshot=wl_snapshot,
                    notes=f"Auto-waitlisted (DISCRETE_WINDOWS full): {overlap_err}",
                )
                return ResponseSuccessSchema(
                    success=True,
                    message=f"Slot occupied — added to waitlist (entry #{wl_id}). {overlap_err}",
                    data={
                        'waitlist_entry_id': wl_id,
                        'status': 'waitlisted',
                        'amenity_id': amenity_id,
                        'booking_date': booking_date.isoformat(),
                        'start_at': start_at.isoformat(),
                        'end_at': end_at.isoformat(),
                        'guest_count': guest_count,
                    },
                )
            raise

        passed_checks = []
        validator.validate(
            policy=policy,
            condominium_id=condominium_id,
            unit_id=unit_id,
            owner_id=owner_id,
            amenity_id=amenity_id,
            amenity_type=amenity_type,
            guest_count=guest_count,
            booking_date=booking_date,
            start_at=start_at,
            end_at=end_at,
        )

        # Slot capacity check — separate from validate() because it may
        # need to be called independently during reallocation (B5+)
        # B6: If capacity exceeded and waitlist is enabled, insert into waitlist
        try:
            validator.check_slot_capacity(
                policy=policy,
                amenity_id=amenity_id,
                start_at=start_at,
                end_at=end_at,
                guest_count=guest_count,
            )
        except BookingValidationError as cap_err:
            # Slot full → try waitlist (B6)
            if policy.waitlist_mode and policy.waitlist_mode not in ('none', 'disabled'):
                from library.dddpy.core_amenity_bookings.usecase.waitlist_usecase import WaitlistUseCase
                wl_uc = WaitlistUseCase()
                wl_policy_snapshot = validator.build_policy_snapshot(policy)
                wl_id = wl_uc.create_entry(
                    amenity_id=amenity_id,
                    unit_id=unit_id,
                    user_id=owner_id,
                    booking_date=booking_date,
                    requested_start_at=start_at,
                    requested_end_at=end_at,
                    guest_count=guest_count,
                    idempotency_key=idempotency_key,
                    policy_snapshot=wl_policy_snapshot,
                    notes=f"Auto-waitlisted: {cap_err}",
                )
                return ResponseSuccessSchema(
                    success=True,
                    message=f"Slot full — added to waitlist (entry #{wl_id}). {cap_err}",
                    data={
                        'waitlist_entry_id': wl_id,
                        'status': 'waitlisted',
                        'amenity_id': amenity_id,
                        'booking_date': booking_date.isoformat(),
                        'start_at': start_at.isoformat(),
                        'end_at': end_at.isoformat(),
                        'guest_count': guest_count,
                    },
                )
            raise

        # Build check list for audit
        if policy.has_usage_limit():
            passed_checks.append('period_limit')
        if policy.has_active_limit():
            passed_checks.append('active_limit')
        if policy.has_guest_limit():
            passed_checks.append('guest_limit')
        if policy.blocked_dates:
            passed_checks.append('blocked_dates')
        if policy.advance_booking_days is not None:
            passed_checks.append(f'advance_booking:{policy.advance_booking_days}d')
        if policy.cancel_window_hours is not None:
            passed_checks.append(f'cancel_window:{policy.cancel_window_hours}h')
        passed_checks.append(f'eligibility:{policy.eligibility_mode}')
        passed_checks.append(f'slot_mode:{policy.slot_mode}')
        passed_checks.append(f'capacity:{policy.max_capacity_per_slot}')
        if idempotency_key:
            passed_checks.append('idempotency')
        passed_checks.append('overlap')

        # ── Phase 3: Snapshots + entity ───────────────────────────────
        unit_code, owner_name = self._get_unit_and_owner_snapshots(unit_id, owner_id)

        # Determine initial status from policy approval_mode
        #   auto                        → draft (never force approval)
        #   amenity_requires_approval   → defer to amenity.requires_approval flag
        #   admin_only                  → always pending_approval
        if policy.approval_mode == 'admin_only':
            initial_status = 'pending_approval'
        elif policy.approval_mode == 'amenity_requires_approval':
            initial_status = 'pending_approval' if amenity.requires_approval else 'draft'
        else:
            initial_status = 'draft'

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
            guest_count=guest_count,
            allocation_source=allocation_source,
            idempotency_key=idempotency_key,
            policy_snapshot_json=validator.build_policy_snapshot(policy),
            allocation_reason_json=validator.build_allocation_reason(policy, passed_checks),
        )

        booking_id = self._cmd_repo.create(entity)
        entity.id = booking_id
        logger.info(
            f"Booking created id={booking_id} amenity={amenity_id} unit={unit_id} "
            f"guest_count={guest_count} policy_scope={policy.scope_level}"
        )

        # B7: Allocation audit — booking accepted
        from library.dddpy.core_amenity_bookings.usecase.allocation_audit_usecase import AllocationAuditUseCase
        audit_uc = AllocationAuditUseCase()
        audit_uc.record(
            amenity_id=amenity_id,
            decision_type='BOOKING_ACCEPTED',
            decision_reason=f"{policy.scope_level} policy, source={allocation_source}",
            booking_id=booking_id,
            context=validator.build_allocation_reason(policy, passed_checks),
        )

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

        # ── Cancel window enforcement (B4) ──
        from library.dddpy.core_amenity_bookings.usecase.policy_resolver import get_policy_resolver
        from library.dddpy.core_amenity_bookings.usecase.booking_policy_validator import BookingPolicyValidator

        policy = get_policy_resolver().resolve(existing.condominium_id, existing.amenity_id)
        validator = BookingPolicyValidator()
        validator.check_cancel_window(policy, existing.start_at)

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

    # ── Report ────────────────────────────────────────────────────

    def get_report(
        self,
        condominium_id: int,
        building_id: Optional[int] = None,
        amenity_id: Optional[int] = None,
        date_from: Optional[date] = None,
        date_to: Optional[date] = None,
    ) -> ResponseSuccessSchema:
        """
        Generate a detailed booking report for a date range.

        Returns:
        - summary: total bookings, total revenue (fees), total deposits held
        - by_status: count per status
        - by_building: breakdown per building
        - by_amenity: breakdown per amenity
        """
        from sqlalchemy import text

        with session_scope() as session:
            # Build common WHERE clause
            wheres = ["b.condominium_id = :condo_id", "b.deleted_at IS NULL"]
            params: dict = {"condo_id": condominium_id}

            if building_id:
                wheres.append("b.building_id = :building_id")
                params["building_id"] = building_id
            if amenity_id:
                wheres.append("b.amenity_id = :amenity_id")
                params["amenity_id"] = amenity_id
            if date_from:
                wheres.append("b.booking_date >= :date_from")
                params["date_from"] = date_from
            if date_to:
                wheres.append("b.booking_date <= :date_to")
                params["date_to"] = date_to

            where_clause = " AND ".join(wheres)

            # ── Summary ──
            summary = session.execute(
                text(f"""
                    SELECT
                        COUNT(*) AS total_bookings,
                        COALESCE(SUM(b.booking_fee_amount), 0) AS total_fees,
                        COALESCE(SUM(CASE WHEN b.deposit_status IN ('paid','pending')
                            THEN b.security_deposit_amount ELSE 0 END), 0) AS deposits_held,
                        COALESCE(SUM(CASE WHEN b.deposit_status = 'applied'
                            THEN b.security_deposit_amount ELSE 0 END), 0) AS deposits_applied,
                        COALESCE(SUM(CASE WHEN b.deposit_status = 'returned'
                            THEN b.security_deposit_amount ELSE 0 END), 0) AS deposits_returned
                    FROM core_amenity_bookings b
                    WHERE {where_clause}
                """),
                params,
            ).mappings().fetchone()

            # ── By status ──
            by_status = session.execute(
                text(f"""
                    SELECT b.status, COUNT(*) AS count,
                           COALESCE(SUM(b.booking_fee_amount), 0) AS revenue
                    FROM core_amenity_bookings b
                    WHERE {where_clause}
                    GROUP BY b.status
                    ORDER BY COUNT(*) DESC
                """),
                params,
            ).mappings().fetchall()

            # ── By building ──
            by_building = session.execute(
                text(f"""
                    SELECT
                        b.building_id,
                        bld.name AS building_name,
                        COUNT(*) AS bookings,
                        COALESCE(SUM(b.booking_fee_amount), 0) AS revenue,
                        COALESCE(SUM(b.security_deposit_amount), 0) AS deposits
                    FROM core_amenity_bookings b
                    LEFT JOIN core_buildings bld ON bld.id = b.building_id
                    WHERE {where_clause}
                    GROUP BY b.building_id, bld.name
                    ORDER BY revenue DESC
                """),
                params,
            ).mappings().fetchall()

            # ── By amenity ──
            by_amenity = session.execute(
                text(f"""
                    SELECT
                        b.amenity_id,
                        a.name AS amenity_name,
                        COUNT(*) AS bookings,
                        COALESCE(SUM(b.booking_fee_amount), 0) AS revenue,
                        COALESCE(SUM(b.security_deposit_amount), 0) AS deposits
                    FROM core_amenity_bookings b
                    LEFT JOIN core_amenities a ON a.id = b.amenity_id
                    WHERE {where_clause}
                    GROUP BY b.amenity_id, a.name
                    ORDER BY revenue DESC
                """),
                params,
            ).mappings().fetchall()

        return ResponseSuccessSchema(
            success=True,
            message="Booking report generated",
            data={
                "filters": {
                    "condominium_id": condominium_id,
                    "building_id": building_id,
                    "amenity_id": amenity_id,
                    "date_from": date_from.isoformat() if date_from else None,
                    "date_to": date_to.isoformat() if date_to else None,
                },
                "summary": dict(summary) if summary else {},
                "by_status": [dict(r) for r in by_status],
                "by_building": [dict(r) for r in by_building],
                "by_amenity": [dict(r) for r in by_amenity],
            },
        )
