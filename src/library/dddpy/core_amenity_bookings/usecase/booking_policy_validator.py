"""
BookingPolicyValidator — enforces EffectiveAmenityPolicy at booking time.

This is the single point where policy meets booking.
BookingUseCase delegates ALL policy checks here — no if/else spread across use cases.
"""
from datetime import datetime, date, timedelta
from typing import Optional

from sqlalchemy import text

from library.dddpy.shared.mysql.session_manager import session_scope
from library.dddpy.core_amenity_bookings.domain.policy_entity import EffectiveAmenityPolicy
from library.dddpy.core_amenity_bookings.domain.booking_exception import BookingValidationError
from library.dddpy.shared.logging.logging import Logger


logger = Logger("BookingPolicyValidator")


class BookingPolicyValidator:
    """
    Validates a booking request against the resolved EffectiveAmenityPolicy.

    All checks are delegated here so BookingUseCase never interprets policy directly.
    """

    def validate(
        self,
        policy: EffectiveAmenityPolicy,
        condominium_id: int,
        unit_id: int,
        owner_id: int,
        amenity_id: int,
        amenity_type: str,
        guest_count: int,
        booking_date: Optional[date] = None,
        start_at: Optional[datetime] = None,
        end_at: Optional[datetime] = None,
    ) -> None:
        """
        Run all applicable policy validations.

        Raises BookingValidationError on first failure.
        """
        # 1. Eligibility
        self._check_eligibility(policy, condominium_id, unit_id, owner_id)

        # 2. Guest limit
        self._check_guest_limit(policy, guest_count)

        # 4. Blocked dates (B4)
        if booking_date:
            self._check_blocked_dates(policy, booking_date)

        # 5. Advance booking window (B4)
        if start_at and policy.advance_booking_days is not None:
            self._check_advance_booking(policy, start_at)

        # 6. Slot compliance (B4) — enforce slot_mode rules
        if start_at and end_at:
            self._check_slot_compliance(policy, start_at, end_at, booking_date)

        # 7. Active reservation limit
        if policy.has_active_limit():
            self._check_active_limit(policy, condominium_id, unit_id, amenity_id, amenity_type)

        # 8. Period reservation limit
        if policy.has_usage_limit():
            self._check_period_limit(policy, condominium_id, unit_id, amenity_id, amenity_type)

    # ── Idempotency ───────────────────────────────────────────────────

    def _check_idempotency(self, condominium_id: int, idempotency_key: str) -> None:
        """Reject if a booking with this idempotency key already exists."""
        with session_scope() as session:
            row = session.execute(
                text("""
                    SELECT id, status FROM core_amenity_bookings
                    WHERE condominium_id = :condo_id
                      AND idempotency_key = :key
                      AND deleted_at IS NULL
                    LIMIT 1
                """),
                {'condo_id': condominium_id, 'key': idempotency_key},
            ).fetchone()

            if row:
                raise BookingValidationError(
                    f"Duplicate request: booking id={row[0]} already exists "
                    f"with idempotency_key='{idempotency_key}' (status={row[1]})"
                )

    # ── Eligibility ───────────────────────────────────────────────────

    def _check_eligibility(
        self,
        policy: EffectiveAmenityPolicy,
        condominium_id: int,
        unit_id: int,
        owner_id: int,
    ) -> None:
        """Check if the user is eligible to book under this policy."""
        mode = policy.eligibility_mode

        if mode == 'all_residents':
            return  # No restriction

        if mode == 'owner_only':
            self._require_ownership(unit_id, owner_id)

        elif mode == 'good_standing_only':
            self._require_ownership(unit_id, owner_id)
            self._require_good_standing(condominium_id, unit_id, owner_id)

        elif mode == 'owner_or_tenant':
            self._require_ownership_or_occupancy(unit_id, owner_id)

        elif mode == 'admin_override':
            return  # Admin bypass — caller is responsible for auth check

        else:
            logger.warning(f"Unknown eligibility_mode='{mode}', defaulting to allow")
            return

    def _require_ownership(self, unit_id: int, owner_id: int) -> None:
        with session_scope() as session:
            row = session.execute(
                text("""
                    SELECT 1 FROM core_unit_ownerships
                    WHERE unit_id = :unit_id
                      AND user_id = :owner_id
                      AND deleted_at IS NULL
                    LIMIT 1
                """),
                {'unit_id': unit_id, 'owner_id': owner_id},
            ).fetchone()

            if not row:
                raise BookingValidationError(
                    f"User id={owner_id} does not own unit id={unit_id}. "
                    f"Policy requires ownership."
                )

    def _require_good_standing(
        self, condominium_id: int, unit_id: int, owner_id: int
    ) -> None:
        """Check no overdue ARs for this unit."""
        with session_scope() as session:
            row = session.execute(
                text("""
                    SELECT COUNT(*) FROM core_accounts_receivable
                    WHERE condominium_id = :condo_id
                      AND unit_id = :unit_id
                      AND debtor_user_id = :owner_id
                      AND status = 'pending'
                      AND due_date < :today
                      AND deleted_at IS NULL
                """),
                {
                    'condo_id': condominium_id,
                    'unit_id': unit_id,
                    'owner_id': owner_id,
                    'today': datetime.utcnow().date(),
                },
            ).fetchone()

            if row and row[0] > 0:
                raise BookingValidationError(
                    f"Unit id={unit_id} has {row[0]} overdue account(s). "
                    f"Policy requires good standing."
                )

    def _require_ownership_or_occupancy(self, unit_id: int, owner_id: int) -> None:
        """User must be either owner or current occupant of the unit."""
        with session_scope() as session:
            row = session.execute(
                text("""
                    SELECT 1 FROM core_unit_ownerships
                    WHERE unit_id = :unit_id
                      AND user_id = :user_id
                      AND deleted_at IS NULL
                    UNION ALL
                    SELECT 1 FROM core_unit_occupancies
                    WHERE unit_id = :unit_id
                      AND user_id = :user_id
                      AND deleted_at IS NULL
                      AND (end_date IS NULL OR end_date >= :today)
                    LIMIT 1
                """),
                {
                    'unit_id': unit_id,
                    'user_id': owner_id,
                    'today': datetime.utcnow().date(),
                },
            ).fetchone()

            if not row:
                raise BookingValidationError(
                    f"User id={owner_id} is neither owner nor active occupant "
                    f"of unit id={unit_id}. Policy requires ownership or occupancy."
                )

    # ── Guest limit ───────────────────────────────────────────────────

    def _check_guest_limit(self, policy: EffectiveAmenityPolicy, guest_count: int) -> None:
        if policy.max_guests is not None and guest_count > policy.max_guests:
            raise BookingValidationError(
                f"Guest count {guest_count} exceeds policy limit "
                f"of {policy.max_guests} for this amenity."
            )

    # ── Scoped counting helpers ───────────────────────────────────────

    def _scope_filter(
        self,
        policy: EffectiveAmenityPolicy,
        field: str,
        amenity_id: int,
        amenity_type: str,
    ) -> tuple[str, dict]:
        """
        Build a WHERE clause fragment and params for scoped enforcement.

        Provenance → enforcement universe:
          CONDOMINIUM  → count all amenity types (whole condo)
          AMENITY_TYPE → count only bookings of same amenity_type
          AMENITY      → count only bookings of this specific amenity
        """
        provenance = policy.field_provenance.get(field, 'CONDOMINIUM')

        if provenance == 'AMENITY':
            return (
                ' AND b.amenity_id = :scope_amenity_id',
                {'scope_amenity_id': amenity_id},
            )
        elif provenance == 'AMENITY_TYPE':
            return (
                ' AND b.amenity_id IN (SELECT a.id FROM core_amenities a WHERE a.amenity_type = :scope_amenity_type AND a.deleted_at IS NULL)',
                {'scope_amenity_type': amenity_type},
            )
        else:
            # CONDOMINIUM (or unknown) → all amenity types
            return ('', {})

    # ── Active reservation limit ──────────────────────────────────────

    def _check_active_limit(
        self,
        policy: EffectiveAmenityPolicy,
        condominium_id: int,
        unit_id: int,
        amenity_id: int,
        amenity_type: str,
    ) -> None:
        """Reject if the unit already has max_active_reservations active bookings."""
        scope_clause, scope_params = self._scope_filter(
            policy, 'max_active_reservations', amenity_id, amenity_type,
        )

        with session_scope() as session:
            row = session.execute(
                text(f"""
                    SELECT COUNT(*) FROM core_amenity_bookings b
                    WHERE b.condominium_id = :condo_id
                      AND b.unit_id = :unit_id
                      AND b.status IN ('draft', 'pending_approval', 'confirmed')
                      AND b.deleted_at IS NULL
                      {scope_clause}
                """),
                {'condo_id': condominium_id, 'unit_id': unit_id, **scope_params},
            ).fetchone()

            count = row[0] if row else 0
            provenance = policy.field_provenance.get('max_active_reservations', 'CONDOMINIUM')
            if count >= policy.max_active_reservations:
                raise BookingValidationError(
                    f"Unit id={unit_id} already has {count} active booking(s) "
                    f"(scope={provenance}). Policy limit is {policy.max_active_reservations}."
                )

    # ── Period reservation limit ──────────────────────────────────────

    def _check_period_limit(
        self,
        policy: EffectiveAmenityPolicy,
        condominium_id: int,
        unit_id: int,
        amenity_id: int,
        amenity_type: str,
    ) -> None:
        """Reject if the unit has exceeded max_reservations_per_period."""
        window_start = self._period_window_start(policy)
        scope_clause, scope_params = self._scope_filter(
            policy, 'max_reservations_per_period', amenity_id, amenity_type,
        )

        with session_scope() as session:
            row = session.execute(
                text(f"""
                    SELECT COUNT(*) FROM core_amenity_bookings b
                    WHERE b.condominium_id = :condo_id
                      AND b.unit_id = :unit_id
                      AND b.status IN ('draft', 'pending_approval', 'confirmed')
                      AND b.created_at >= :window_start
                      AND b.deleted_at IS NULL
                      {scope_clause}
                """),
                {
                    'condo_id': condominium_id,
                    'unit_id': unit_id,
                    'window_start': window_start,
                    **scope_params,
                },
            ).fetchone()

            count = row[0] if row else 0
            provenance = policy.field_provenance.get('max_reservations_per_period', 'CONDOMINIUM')
            if count >= policy.max_reservations_per_period:
                raise BookingValidationError(
                    f"Unit id={unit_id} has {count} booking(s) in the last "
                    f"{policy.period_value} {policy.period_unit}(s) "
                    f"(scope={provenance}). "
                    f"Policy limit is {policy.max_reservations_per_period}."
                )

    def _period_window_start(self, policy: EffectiveAmenityPolicy) -> datetime:
        """Calculate the start of the evaluation window for period limits."""
        now = datetime.utcnow()
        unit = policy.period_unit
        value = policy.period_value or 1

        if unit == 'day':
            return now - timedelta(days=value)
        elif unit == 'week':
            return now - timedelta(weeks=value)
        elif unit == 'month':
            # Approximate: subtract 30*value days
            return now - timedelta(days=30 * value)
        elif unit == 'quarter':
            return now - timedelta(days=90 * value)
        else:
            # Default to month
            return now - timedelta(days=30)

    # ── Slot compliance (B4) ──────────────────────────────────────────

    def _check_slot_compliance(
        self,
        policy: EffectiveAmenityPolicy,
        start_at: datetime,
        end_at: datetime,
        booking_date: Optional[date] = None,
    ) -> None:
        """
        Enforce slot_mode rules:

        CONTINUOUS_SLOTS:
          - Booking duration must be a multiple of slot_interval_min

        DISCRETE_WINDOWS:
          - start_at.time >= window_start_time
          - end_at.time <= window_end_time
          - booking date must be within opening_hours day of week
        """
        if policy.slot_mode == 'DISCRETE_WINDOWS':
            self._check_discrete_window(policy, start_at, end_at, booking_date)
        elif policy.slot_mode == 'CONTINUOUS_SLOTS':
            self._check_continuous_slot(policy, start_at, end_at)

    def _check_continuous_slot(
        self,
        policy: EffectiveAmenityPolicy,
        start_at: datetime,
        end_at: datetime,
    ) -> None:
        """For CONTINUOUS_SLOTS, booking duration must align with slot_interval_min."""
        if policy.slot_interval_min is None:
            return
        duration_min = int((end_at - start_at).total_seconds() / 60)
        if duration_min % policy.slot_interval_min != 0:
            raise BookingValidationError(
                f"Booking duration ({duration_min}min) must be a multiple of "
                f"slot_interval_min ({policy.slot_interval_min}min)."
            )

    def _check_discrete_window(
        self,
        policy: EffectiveAmenityPolicy,
        start_at: datetime,
        end_at: datetime,
        booking_date: Optional[date] = None,
    ) -> None:
        """For DISCRETE_WINDOWS, booking must fit within the defined time window."""
        if policy.window_start_time and policy.window_end_time:
            start_t = start_at.time()
            end_t = end_at.time()
            ws = self._parse_time(policy.window_start_time)
            we = self._parse_time(policy.window_end_time)
            if ws and we:
                if start_t < ws or end_t > we:
                    raise BookingValidationError(
                        f"Booking ({start_t} - {end_t}) outside allowed window "
                        f"({policy.window_start_time} - {policy.window_end_time})."
                    )

        # Check opening_hours by day of week
        if booking_date and policy.opening_hours_json:
            day_name = booking_date.strftime('%A').lower()
            day_hours = policy.opening_hours_json.get(day_name)
            if day_hours:
                open_t = self._parse_time(day_hours.get('open'))
                close_t = self._parse_time(day_hours.get('close'))
                if open_t and close_t:
                    if start_at.time() < open_t or end_at.time() > close_t:
                        raise BookingValidationError(
                            f"Booking outside operating hours for {day_name} "
                            f"({day_hours.get('open')} - {day_hours.get('close')})."
                        )

    @staticmethod
    def _parse_time(time_str: Optional[str]):
        """Parse 'HH:MM' or 'HH:MM:SS' string to time object."""
        if not time_str:
            return None
        from datetime import time as dt_time
        for fmt in ('%H:%M:%S', '%H:%M'):
            try:
                return datetime.strptime(time_str, fmt).time()
            except ValueError:
                continue
        return None

    # ── Availability validations (B4) ─────────────────────────────────

    def _check_blocked_dates(
        self,
        policy: EffectiveAmenityPolicy,
        booking_date: date,
    ) -> None:
        """Reject if the booking date is in blocked_dates."""
        blocked = policy.blocked_dates
        if not blocked:
            return
        date_str = booking_date.isoformat()
        if date_str in blocked:
            raise BookingValidationError(
                f"Date {date_str} is blocked for this amenity."
            )

    def _check_advance_booking(
        self,
        policy: EffectiveAmenityPolicy,
        start_at: datetime,
    ) -> None:
        """Reject if booking is further out than advance_booking_days allows."""
        max_future = datetime.utcnow() + timedelta(days=policy.advance_booking_days)
        if start_at > max_future:
            raise BookingValidationError(
                f"Booking starts {start_at.isoformat()}, but advance limit is "
                f"{policy.advance_booking_days} days (max {max_future.isoformat()})."
            )

    def check_cancel_window(
        self,
        policy: EffectiveAmenityPolicy,
        start_at: datetime,
    ) -> None:
        """
        Public method — called during cancel flow.
        Reject cancellation if it's too close to the booking start.
        """
        if policy.cancel_window_hours is None:
            return  # No restriction
        deadline = start_at - timedelta(hours=policy.cancel_window_hours)
        if datetime.utcnow() > deadline:
            raise BookingValidationError(
                f"Cannot cancel: less than {policy.cancel_window_hours}h before start. "
                f"Deadline was {deadline.isoformat()}."
            )

    def check_slot_capacity(
        self,
        policy: EffectiveAmenityPolicy,
        amenity_id: int,
        start_at: datetime,
        end_at: datetime,
        guest_count: int,
        exclude_booking_id: Optional[int] = None,
    ) -> None:
        """
        Verify slot capacity before allocation.

        DISCRETE_WINDOWS: max_capacity_per_slot = max concurrent BOOKINGS.
          Count overlapping bookings, reject if at limit.

        CONTINUOUS_SLOTS: max_capacity_per_slot = max total GUESTS.
          Sum guest_counts of overlapping bookings, reject if overflow.
        """
        with session_scope() as session:
            params = {
                'amenity_id': amenity_id,
                'start_at': start_at,
                'end_at': end_at,
            }
            exclude = ''
            if exclude_booking_id:
                exclude = ' AND b.id != :exclude_id'
                params['exclude_id'] = exclude_booking_id

            if policy.slot_mode == 'DISCRETE_WINDOWS':
                # Count overlapping bookings (not guests) — exclusive amenity
                row = session.execute(
                    text(f"""
                        SELECT COUNT(*) FROM core_amenity_bookings b
                        WHERE b.amenity_id = :amenity_id
                          AND b.status IN ('draft', 'pending_approval', 'confirmed')
                          AND b.deleted_at IS NULL
                          AND b.start_at < :end_at
                          AND b.end_at > :start_at
                          {exclude}
                    """),
                    params,
                ).fetchone()
                count = int(row[0]) if row else 0
                if count >= policy.max_capacity_per_slot:
                    raise BookingValidationError(
                        f"Slot capacity exceeded: {count} booking(s) already exist, "
                        f"max {policy.max_capacity_per_slot} allowed (DISCRETE_WINDOWS)."
                    )
            else:
                # Sum guest_counts — shared amenity
                row = session.execute(
                    text(f"""
                        SELECT COALESCE(SUM(b.guest_count), 0) AS total_guests
                        FROM core_amenity_bookings b
                        WHERE b.amenity_id = :amenity_id
                          AND b.status IN ('draft', 'pending_approval', 'confirmed')
                          AND b.deleted_at IS NULL
                          AND b.start_at < :end_at
                          AND b.end_at > :start_at
                          {exclude}
                    """),
                    params,
                ).fetchone()

                current_guests = int(row[0]) if row else 0
                if current_guests + guest_count > policy.max_capacity_per_slot:
                    raise BookingValidationError(
                        f"Slot capacity exceeded: {current_guests} guests already booked, "
                        f"adding {guest_count} would exceed max {policy.max_capacity_per_slot}."
                    )

    # ── Snapshot ──────────────────────────────────────────────────────

    def build_policy_snapshot(self, policy: EffectiveAmenityPolicy) -> dict:
        """Serialize the effective policy for storage in policy_snapshot_json."""
        return policy.to_dict()

    def build_allocation_reason(
        self,
        policy: EffectiveAmenityPolicy,
        passed_checks: list[str],
    ) -> dict:
        """Build allocation_reason_json with audit data."""
        return {
            'policy_scope': policy.scope_level,
            'policy_source_ids': policy.source_policy_ids,
            'passed_checks': passed_checks,
            'resolved_at': datetime.utcnow().isoformat(),
        }
