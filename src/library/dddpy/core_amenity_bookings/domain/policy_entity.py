"""
EffectiveAmenityPolicy — resolved policy value object.

This is the single source of truth for policy decisions.
No use case may interpret raw policy rows directly.
"""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Optional


# ── Defaults applied when no policy row covers a field ──

POLICY_DEFAULTS = {
    'eligibility_mode': 'all_residents',
    'max_reservations_per_period': None,
    'period_unit': None,
    'period_value': None,
    'max_active_reservations': None,
    'max_guests': None,
    'priority_policy': 'fifo',
    'priority_window_unit': None,
    'priority_window_value': None,
    'waitlist_mode': None,  # None = disabled; must be explicitly configured
    'approval_mode': 'auto',
    'blocked_dates': [],
    'advance_booking_days': None,
    'cancel_window_hours': None,
    'slot_mode': 'CONTINUOUS_SLOTS',
    'slot_interval_min': None,
    'max_capacity_per_slot': None,
    'extra_rules_json': {},
}

# Fields that MUST NOT be None after resolution (always have a default)
_NON_NULLABLE = {'eligibility_mode', 'priority_policy', 'approval_mode', 'slot_mode'}


@dataclass
class EffectiveAmenityPolicy:
    """
    Fully-resolved policy for a specific amenity in a condominium.

    Created by PolicyResolver.merge() from the cascade:
        CONDOMINIUM → AMENITY_TYPE → AMENITY

    Rule: a non-None value at a lower scope overrides the higher scope
    for that field ONLY. Missing fields inherit from the level above.
    """

    scope_level: str = 'CONDOMINIUM'

    # ── Eligibility ──
    eligibility_mode: str = 'all_residents'

    # ── Usage limits ──
    max_reservations_per_period: Optional[int] = None
    period_unit: Optional[str] = None
    period_value: Optional[int] = None
    max_active_reservations: Optional[int] = None
    max_guests: Optional[int] = None

    # ── Priority ──
    priority_policy: str = 'fifo'
    priority_window_unit: Optional[str] = None
    priority_window_value: Optional[int] = None

    # ── Waitlist ──
    waitlist_mode: str = None

    # ── Approval ──
    approval_mode: str = 'auto'

    # ── Availability (populated from availability_rules when B4 is done) ──
    blocked_dates: list[str] = field(default_factory=list)
    advance_booking_days: Optional[int] = None
    cancel_window_hours: Optional[int] = None
    slot_mode: str = 'CONTINUOUS_SLOTS'
    slot_interval_min: Optional[int] = None
    window_start_time: Optional[str] = None
    window_end_time: Optional[str] = None
    max_capacity_per_slot: Optional[int] = None
    opening_hours_json: dict = field(default_factory=dict)

    # ── Extensions ──
    extra_rules_json: dict = field(default_factory=dict)

    # ── Metadata ──
    source_policy_ids: list[int] = field(default_factory=list)
    """IDs of the policy rows that contributed to this resolution (for audit)."""

    field_provenance: dict[str, str] = field(default_factory=dict)
    """
    Which scope_level supplied each field. Used by validators to build
    correctly-scoped enforcement queries (e.g. CONDOMINIUM-level limit
    counts all amenity types; AMENITY_TYPE counts only matching type).
    
    Example:
        {'max_reservations_per_period': 'CONDOMINIUM',
         'max_active_reservations': 'AMENITY_TYPE',
         'max_guests': 'AMENITY'}
    """

    @classmethod
    def default(cls) -> 'EffectiveAmenityPolicy':
        """Return a policy with all system defaults (no DB rows resolved)."""
        return cls(
            scope_level='CONDOMINIUM',
            eligibility_mode='all_residents',
            priority_policy='fifo',
            waitlist_mode=None,  # disabled by default
            approval_mode='auto',
            slot_mode='CONTINUOUS_SLOTS',
        )

    def to_dict(self) -> dict:
        return {
            'scope_level': self.scope_level,
            'eligibility_mode': self.eligibility_mode,
            'max_reservations_per_period': self.max_reservations_per_period,
            'period_unit': self.period_unit,
            'period_value': self.period_value,
            'max_active_reservations': self.max_active_reservations,
            'max_guests': self.max_guests,
            'priority_policy': self.priority_policy,
            'priority_window_unit': self.priority_window_unit,
            'priority_window_value': self.priority_window_value,
            'waitlist_mode': self.waitlist_mode,
            'approval_mode': self.approval_mode,
            'blocked_dates': self.blocked_dates,
            'advance_booking_days': self.advance_booking_days,
            'cancel_window_hours': self.cancel_window_hours,
            'slot_mode': self.slot_mode,
            'slot_interval_min': self.slot_interval_min,
            'window_start_time': self.window_start_time,
            'window_end_time': self.window_end_time,
            'max_capacity_per_slot': self.max_capacity_per_slot,
            'opening_hours_json': self.opening_hours_json,
            'extra_rules_json': self.extra_rules_json,
            'source_policy_ids': self.source_policy_ids,
            'field_provenance': self.field_provenance,
        }

    def has_usage_limit(self) -> bool:
        """True if a per-period reservation limit is configured."""
        return (
            self.max_reservations_per_period is not None
            and self.period_unit is not None
            and self.period_value is not None
        )

    def has_active_limit(self) -> bool:
        """True if an active reservation limit is configured."""
        return self.max_active_reservations is not None

    def has_guest_limit(self) -> bool:
        """True if guest count is limited."""
        return self.max_guests is not None

    def requires_approval(self) -> bool:
        """
        Resolve whether approval is required.

        Semantics:
          - auto → never require approval
          - amenity_requires_approval → defer to the amenity's requires_approval flag
          - admin_only → always require approval
        """
        return self.approval_mode == 'admin_only'

    def approval_defers_to_amenity(self) -> bool:
        """True if approval_mode tells us to check the amenity flag."""
        return self.approval_mode == 'amenity_requires_approval'
