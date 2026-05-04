"""
PolicyResolver — single point of policy resolution.

Resolves the cascade CONDOMINIUM → AMENITY_TYPE → AMENITY
and returns a single EffectiveAmenityPolicy.

No use case should query core_amenity_policies directly.
"""
from datetime import datetime
from typing import Optional, List

from sqlalchemy import text

from library.dddpy.shared.mysql.session_manager import session_scope
from library.dddpy.core_amenity_bookings.domain.policy_entity import (
    EffectiveAmenityPolicy,
    POLICY_DEFAULTS,
)
from library.dddpy.shared.logging.logging import Logger


logger = Logger("PolicyResolver")

# ── Fields that are mergeable (mapped from DB column → EffectiveAmenityPolicy attr) ──

_MERGEABLE_FIELDS = [
    'eligibility_mode',
    'max_reservations_per_period',
    'period_unit',
    'period_value',
    'max_active_reservations',
    'max_guests',
    'priority_policy',
    'priority_window_unit',
    'priority_window_value',
    'waitlist_mode',
    'approval_mode',
    'extra_rules_json',
]

# Fields that come from the availability layer (B4), not from policies
_AVAILABILITY_FIELDS = {
    'slot_mode', 'slot_interval_min', 'max_capacity_per_slot',
    'advance_booking_days', 'cancel_window_hours', 'blocked_dates',
}


class PolicyResolver:
    """
    Resolves the effective policy for an amenity by merging the cascade:

        1. CONDOMINIUM-level policies (global)
        2. AMENITY_TYPE-level policies (per amenity category)
        3. AMENITY-level policies (per specific instance)

    Lower levels override higher levels only for explicitly set (non-null) fields.
    """

    # ── Public API ────────────────────────────────────────────────────

    def resolve(
        self,
        condominium_id: int,
        amenity_id: int,
    ) -> EffectiveAmenityPolicy:
        """
        Resolve the effective policy for a specific amenity.

        Args:
            condominium_id: The condominium scope.
            amenity_id: The specific amenity being booked.

        Returns:
            EffectiveAmenityPolicy with all fields resolved.
        """
        logger.info(f"Resolving policy for condo={condominium_id} amenity={amenity_id}")

        # 1. Resolve amenity → amenity_type
        amenity_type = self._lookup_amenity_type(amenity_id)

        # 2. Fetch all relevant policy rows (active only)
        rows = self._fetch_policies(condominium_id, amenity_type, amenity_id)

        # 3. Merge cascade
        policy = self._merge(rows)

        # 4. Enrich with amenity-level defaults from core_amenities
        self._enrich_from_amenity(policy, amenity_id)

        logger.info(
            f"Resolved policy scope={policy.scope_level} "
            f"sources={policy.source_policy_ids} "
            f"approval={policy.approval_mode} priority={policy.priority_policy}"
        )
        return policy

    def resolve_for_type(
        self,
        condominium_id: int,
        amenity_type: str,
    ) -> EffectiveAmenityPolicy:
        """
        Resolve policy for an amenity type (without a specific amenity_id).
        Useful for admin UIs showing type-level defaults.
        """
        rows = self._fetch_policies(condominium_id, amenity_type, amenity_id=None)
        return self._merge(rows)

    # ── Internal ──────────────────────────────────────────────────────

    def _lookup_amenity_type(self, amenity_id: int) -> str:
        """Look up amenity_type from core_amenities (column added in 063)."""
        with session_scope() as session:
            row = session.execute(
                text("""
                    SELECT amenity_type FROM core_amenities
                    WHERE id = :amenity_id AND deleted_at IS NULL
                """),
                {'amenity_id': amenity_id},
            ).fetchone()

            if not row:
                raise ValueError(f"Amenity id={amenity_id} not found")

            amenity_type = row[0]
            if not amenity_type:
                raise ValueError(
                    f"Amenity id={amenity_id} has no amenity_type configured. "
                    f"Run migration 063 backfill or set it manually."
                )
            return amenity_type

    def _fetch_policies(
        self,
        condominium_id: int,
        amenity_type: str,
        amenity_id: Optional[int],
    ) -> List[dict]:
        """
        Fetch all active policy rows that apply to the cascade.

        Returns rows in cascade order: CONDOMINIUM, AMENITY_TYPE, AMENITY.
        """
        with session_scope() as session:
            rows = session.execute(
                text("""
                    SELECT
                        id, scope_level, amenity_type, amenity_id,
                        eligibility_mode,
                        max_reservations_per_period, period_unit, period_value,
                        max_active_reservations, max_guests,
                        priority_policy, priority_window_unit, priority_window_value,
                        waitlist_mode, approval_mode,
                        extra_rules_json
                    FROM core_amenity_policies
                    WHERE condominium_id = :condo_id
                      AND is_active = 1
                      AND (
                          -- Global
                          (scope_level = 'CONDOMINIUM')
                          -- Type match
                          OR (scope_level = 'AMENITY_TYPE' AND amenity_type = :amenity_type)
                          -- Specific amenity override
                          OR (scope_level = 'AMENITY' AND amenity_id = :amenity_id)
                      )
                    ORDER BY
                        FIELD(scope_level, 'CONDOMINIUM', 'AMENITY_TYPE', 'AMENITY')
                """),
                {
                    'condo_id': condominium_id,
                    'amenity_type': amenity_type,
                    'amenity_id': amenity_id,
                },
            ).mappings().fetchall()

            return [dict(r) for r in rows]

    def _merge(self, rows: List[dict]) -> EffectiveAmenityPolicy:
        """
        Merge policy rows using cascade precedence.

        Start with system defaults, then apply each level
        (CONDOMINIUM → AMENITY_TYPE → AMENITY).
        A non-None value at a lower level overrides the level above.
        """
        merged = dict(POLICY_DEFAULTS)
        source_ids: List[int] = []
        field_provenance: dict[str, str] = {}

        for row in rows:
            source_ids.append(row['id'])
            scope = row['scope_level']

            for field in _MERGEABLE_FIELDS:
                value = row.get(field)
                if value is not None:
                    # Special handling for JSON fields that may be empty dicts
                    if field == 'extra_rules_json' and isinstance(value, dict) and len(value) == 0:
                        continue
                    merged[field] = value
                    field_provenance[field] = scope

            # Track the deepest scope level applied
            merged['scope_level'] = scope

        # Reconstruct extra_rules_json as dict if None
        if merged.get('extra_rules_json') is None:
            merged['extra_rules_json'] = {}

        # Ensure non-nullable fields have values (waitlist_mode excluded — None = disabled)
        for field in ('eligibility_mode', 'priority_policy', 'approval_mode'):
            if merged.get(field) is None:
                merged[field] = POLICY_DEFAULTS[field]

        # Remove availability fields from extra_rules_json if they leaked in
        # (they belong in availability_rules, B4)
        extra = merged.get('extra_rules_json', {})
        for avail_field in _AVAILABILITY_FIELDS:
            extra.pop(avail_field, None)

        return EffectiveAmenityPolicy(
            scope_level=merged.get('scope_level', 'CONDOMINIUM'),
            eligibility_mode=merged.get('eligibility_mode', 'all_residents'),
            max_reservations_per_period=merged.get('max_reservations_per_period'),
            period_unit=merged.get('period_unit'),
            period_value=merged.get('period_value'),
            max_active_reservations=merged.get('max_active_reservations'),
            max_guests=merged.get('max_guests'),
            priority_policy=merged.get('priority_policy', 'fifo'),
            priority_window_unit=merged.get('priority_window_unit'),
            priority_window_value=merged.get('priority_window_value'),
            waitlist_mode=merged.get('waitlist_mode'),  # None means disabled — no default
            approval_mode=merged.get('approval_mode', 'auto'),
            blocked_dates=merged.get('blocked_dates', []),
            advance_booking_days=merged.get('advance_booking_days'),
            cancel_window_hours=merged.get('cancel_window_hours'),
            slot_mode=merged.get('slot_mode', 'CONTINUOUS_SLOTS'),
            slot_interval_min=merged.get('slot_interval_min'),
            max_capacity_per_slot=merged.get('max_capacity_per_slot'),
            extra_rules_json=merged.get('extra_rules_json', {}),
            source_policy_ids=source_ids,
            field_provenance=field_provenance,
        )

    def _enrich_from_amenity(
        self,
        policy: EffectiveAmenityPolicy,
        amenity_id: int,
    ) -> None:
        """
        Enrich the policy with amenity-level defaults from core_amenities
        AND availability rules from core_amenity_availability_rules.

        Availability rules override amenity defaults where both exist.
        """
        with session_scope() as session:
            # ── Amenity base fields ──
            amenity_row = session.execute(
                text("""
                    SELECT
                        max_capacity,
                        booking_duration_min,
                        requires_approval,
                        is_reservable
                    FROM core_amenities
                    WHERE id = :amenity_id AND deleted_at IS NULL
                """),
                {'amenity_id': amenity_id},
            ).fetchone()

            if not amenity_row:
                return

            # ── Availability rules (override amenity defaults) ──
            avail_row = session.execute(
                text("""
                    SELECT
                        slot_mode, slot_interval_min,
                        window_start_time, window_end_time,
                        max_capacity_per_slot,
                        advance_booking_days, cancel_window_hours,
                        blocked_dates_json, opening_hours_json
                    FROM core_amenity_availability_rules
                    WHERE amenity_id = :amenity_id AND is_active = 1
                """),
                {'amenity_id': amenity_id},
            ).fetchone()

            # ── Apply availability rules first (they are explicit config) ──
            if avail_row:
                if avail_row[0] is not None:
                    policy.slot_mode = avail_row[0]
                if avail_row[1] is not None:
                    policy.slot_interval_min = int(avail_row[1])
                if avail_row[2] is not None:
                    policy.window_start_time = str(avail_row[2])
                if avail_row[3] is not None:
                    policy.window_end_time = str(avail_row[3])
                if avail_row[4] is not None:
                    policy.max_capacity_per_slot = int(avail_row[4])
                if avail_row[5] is not None:
                    policy.advance_booking_days = int(avail_row[5])
                if avail_row[6] is not None:
                    policy.cancel_window_hours = int(avail_row[6])
                if avail_row[7] is not None:
                    policy.blocked_dates = list(avail_row[7]) if isinstance(avail_row[7], list) else []
                if avail_row[8] is not None:
                    policy.opening_hours_json = dict(avail_row[8]) if isinstance(avail_row[8], dict) else {}
                return  # availability rules are authoritative, skip amenity fallbacks

            # ── Fallback to amenity base fields (no availability rules row) ──
            if policy.max_capacity_per_slot is None and amenity_row[0] is not None:
                policy.max_capacity_per_slot = int(amenity_row[0])
            if policy.slot_interval_min is None and amenity_row[1] is not None:
                policy.slot_interval_min = int(amenity_row[1])


# ── Module-level singleton (optional, can also be instantiated per use case) ──

_policy_resolver: Optional[PolicyResolver] = None


def get_policy_resolver() -> PolicyResolver:
    """Return the module-level PolicyResolver singleton."""
    global _policy_resolver
    if _policy_resolver is None:
        _policy_resolver = PolicyResolver()
    return _policy_resolver
