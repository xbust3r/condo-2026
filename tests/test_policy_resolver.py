"""
Unit tests: PolicyResolver — cascade merge + defaults.

Covers:
- Empty policies → system defaults
- Single CONDOMINIUM-level policy
- CONDOMINIUM + AMENITY_TYPE merge (override)
- Full cascade CONDOMINIUM → AMENITY_TYPE → AMENITY
- NULL fields inherit from upper level
- source_policy_ids tracking
- amenity enrichment (max_capacity, booking_duration_min)
"""
import pytest
from unittest.mock import MagicMock, patch
from datetime import datetime

from library.dddpy.core_amenity_bookings.domain.policy_entity import (
    EffectiveAmenityPolicy,
    POLICY_DEFAULTS,
)
from library.dddpy.core_amenity_bookings.usecase.policy_resolver import PolicyResolver


# ── Helpers ──────────────────────────────────────────────────────────────

def _make_row(**overrides):
    """Build a mock policy DB row."""
    defaults = {
        'id': 1,
        'scope_level': 'CONDOMINIUM',
        'amenity_type': None,
        'amenity_id': None,
        'eligibility_mode': None,
        'max_reservations_per_period': None,
        'period_unit': None,
        'period_value': None,
        'max_active_reservations': None,
        'max_guests': None,
        'priority_policy': None,
        'priority_window_unit': None,
        'priority_window_value': None,
        'waitlist_mode': None,
        'approval_mode': None,
        'extra_rules_json': None,
    }
    defaults.update(overrides)
    return defaults


# ── EffectiveAmenityPolicy ───────────────────────────────────────────────

class TestEffectiveAmenityPolicy:
    def test_default_has_sensible_values(self):
        p = EffectiveAmenityPolicy.default()
        assert p.eligibility_mode == 'all_residents'
        assert p.priority_policy == 'fifo'
        assert p.waitlist_mode is None  # None = disabled by default
        assert p.approval_mode == 'auto'
        assert p.slot_mode == 'CONTINUOUS_SLOTS'

    def test_has_usage_limit_false_when_missing(self):
        p = EffectiveAmenityPolicy.default()
        assert not p.has_usage_limit()

    def test_has_usage_limit_true_when_complete(self):
        p = EffectiveAmenityPolicy(
            max_reservations_per_period=3,
            period_unit='month',
            period_value=1,
        )
        assert p.has_usage_limit()

    def test_has_usage_limit_false_when_incomplete(self):
        p = EffectiveAmenityPolicy(max_reservations_per_period=3)
        assert not p.has_usage_limit()

    def test_has_active_limit(self):
        p = EffectiveAmenityPolicy(max_active_reservations=2)
        assert p.has_active_limit()

    def test_has_guest_limit(self):
        p = EffectiveAmenityPolicy(max_guests=5)
        assert p.has_guest_limit()

    def test_requires_approval(self):
        # auto → never requires
        assert not EffectiveAmenityPolicy(approval_mode='auto').requires_approval()
        # amenity_requires_approval → defers to amenity flag (not forced)
        assert not EffectiveAmenityPolicy(approval_mode='amenity_requires_approval').requires_approval()
        assert EffectiveAmenityPolicy(approval_mode='amenity_requires_approval').approval_defers_to_amenity()
        # admin_only → always forces approval
        assert EffectiveAmenityPolicy(approval_mode='admin_only').requires_approval()
        assert not EffectiveAmenityPolicy(approval_mode='admin_only').approval_defers_to_amenity()

    def test_to_dict_includes_all_fields(self):
        p = EffectiveAmenityPolicy.default()
        d = p.to_dict()
        assert 'scope_level' in d
        assert 'source_policy_ids' in d
        assert 'blocked_dates' in d
        assert isinstance(d['blocked_dates'], list)


# ── PolicyResolver._merge ─────────────────────────────────────────────────

class TestPolicyResolverMerge:
    def setup_method(self):
        self.resolver = PolicyResolver()

    def test_empty_rows_returns_defaults(self):
        result = self.resolver._merge([])
        assert result.eligibility_mode == 'all_residents'
        assert result.priority_policy == 'fifo'
        assert result.waitlist_mode is None  # None = disabled by default
        assert result.approval_mode == 'auto'
        assert result.source_policy_ids == []

    def test_single_condominium_row_applies_all(self):
        rows = [
            _make_row(
                id=1,
                scope_level='CONDOMINIUM',
                eligibility_mode='owner_only',
                max_reservations_per_period=2,
                period_unit='month',
                period_value=1,
                max_active_reservations=1,
                priority_policy='less_usage_first',
                priority_window_unit='month',
                priority_window_value=3,
                waitlist_mode='auto_confirm',
                approval_mode='admin_only',
            ),
        ]
        result = self.resolver._merge(rows)
        assert result.eligibility_mode == 'owner_only'
        assert result.max_reservations_per_period == 2
        assert result.period_unit == 'month'
        assert result.period_value == 1
        assert result.max_active_reservations == 1
        assert result.priority_policy == 'less_usage_first'
        assert result.priority_window_unit == 'month'
        assert result.priority_window_value == 3
        assert result.waitlist_mode == 'auto_confirm'
        assert result.approval_mode == 'admin_only'
        assert result.scope_level == 'CONDOMINIUM'
        assert result.source_policy_ids == [1]

    def test_type_overrides_condominium(self):
        rows = [
            _make_row(
                id=1,
                scope_level='CONDOMINIUM',
                max_reservations_per_period=2,
                priority_policy='fifo',
                eligibility_mode='all_residents',
            ),
            _make_row(
                id=2,
                scope_level='AMENITY_TYPE',
                amenity_type='POOL',
                max_reservations_per_period=4,
                priority_policy='less_usage_first',
                # eligibility_mode=NULL → inherit from CONDOMINIUM
            ),
        ]
        result = self.resolver._merge(rows)
        # Type overrides period limit and priority
        assert result.max_reservations_per_period == 4
        assert result.priority_policy == 'less_usage_first'
        # Inherited from CONDOMINIUM (NULL in type)
        assert result.eligibility_mode == 'all_residents'
        assert result.scope_level == 'AMENITY_TYPE'
        assert result.source_policy_ids == [1, 2]

    def test_amenity_overrides_type(self):
        rows = [
            _make_row(id=1, scope_level='CONDOMINIUM', max_active_reservations=1, max_guests=None),
            _make_row(id=2, scope_level='AMENITY_TYPE', amenity_type='POOL', max_guests=5),
            _make_row(id=3, scope_level='AMENITY', amenity_id=10, max_active_reservations=2, max_guests=8),
        ]
        result = self.resolver._merge(rows)
        # Amenity overrides both upper levels where set
        assert result.max_active_reservations == 2  # from AMENITY
        assert result.max_guests == 8  # from AMENITY (overrides TYPE's 5)
        assert result.scope_level == 'AMENITY'
        assert result.source_policy_ids == [1, 2, 3]

    def test_null_fields_do_not_override(self):
        """Fields set to None at lower level must inherit from upper level."""
        rows = [
            _make_row(
                id=1,
                scope_level='CONDOMINIUM',
                eligibility_mode='good_standing_only',
                max_reservations_per_period=2,
                priority_policy='equal_share',
            ),
            _make_row(
                id=2,
                scope_level='AMENITY_TYPE',
                amenity_type='POOL',
                max_reservations_per_period=4,
                # eligibility_mode=NULL → inherit
                # priority_policy=NULL → inherit
            ),
        ]
        result = self.resolver._merge(rows)
        assert result.max_reservations_per_period == 4  # overridden
        assert result.eligibility_mode == 'good_standing_only'  # inherited
        assert result.priority_policy == 'equal_share'  # inherited
        assert result.source_policy_ids == [1, 2]

    def test_extra_rules_json_merge(self):
        rows = [
            _make_row(
                id=1,
                scope_level='CONDOMINIUM',
                extra_rules_json={'custom_rule': 'global_value', 'shared': 'from_global'},
            ),
            _make_row(
                id=2,
                scope_level='AMENITY_TYPE',
                amenity_type='POOL',
                extra_rules_json={'shared': 'from_type', 'type_only': True},
            ),
        ]
        result = self.resolver._merge(rows)
        # Top-level extra_rules_json is overridden entirely (not deep-merged)
        assert result.extra_rules_json == {'shared': 'from_type', 'type_only': True}

    def test_scope_level_tracks_deepest_applied(self):
        rows = [
            _make_row(id=1, scope_level='CONDOMINIUM', max_reservations_per_period=2),
            _make_row(id=2, scope_level='AMENITY_TYPE', amenity_type='POOL'),
        ]
        result = self.resolver._merge(rows)
        assert result.scope_level == 'AMENITY_TYPE'

    def test_merge_preserves_policy_ids_order(self):
        rows = [
            _make_row(id=1, scope_level='CONDOMINIUM'),
            _make_row(id=2, scope_level='AMENITY_TYPE', amenity_type='POOL'),
            _make_row(id=3, scope_level='AMENITY', amenity_id=10),
        ]
        result = self.resolver._merge(rows)
        assert result.source_policy_ids == [1, 2, 3]


# ── Integration: full resolve flow (mocked DB) ────────────────────────────

class TestPolicyResolverResolve:
    """Test resolve() with mocked _fetch_policies and _lookup_amenity_type."""

    def setup_method(self):
        self.resolver = PolicyResolver()

    def test_resolve_full_cascade(self):
        """Simulate a full cascade resolution."""
        # Mock the amenity type lookup
        self.resolver._lookup_amenity_type = MagicMock(return_value='POOL')

        # Mock the policy fetch
        self.resolver._fetch_policies = MagicMock(return_value=[
            _make_row(
                id=1, scope_level='CONDOMINIUM',
                eligibility_mode='all_residents',
                max_reservations_per_period=2,
                period_unit='month', period_value=1,
                max_active_reservations=1,
                priority_policy='fifo',
                waitlist_mode='notify_and_confirm',
                approval_mode='auto',
            ),
            _make_row(
                id=2, scope_level='AMENITY_TYPE', amenity_type='POOL',
                max_reservations_per_period=4,
                max_guests=5,
                priority_policy='less_usage_first',
                priority_window_unit='month', priority_window_value=1,
                # waitlist_mode, approval_mode NULL → inherit
            ),
            _make_row(
                id=3, scope_level='AMENITY', amenity_id=10,
                max_active_reservations=2,
                max_guests=8,
                # max_reservations NULL → inherit from type
                # priority NULL → inherit from type
            ),
        ])

        # Mock enrichment from amenity
        self.resolver._enrich_from_amenity = MagicMock()

        result = self.resolver.resolve(condominium_id=1, amenity_id=10)

        assert result.eligibility_mode == 'all_residents'
        assert result.max_reservations_per_period == 4  # from TYPE
        assert result.period_unit == 'month'  # from CONDOMINIUM
        assert result.period_value == 1
        assert result.max_active_reservations == 2  # from AMENITY
        assert result.max_guests == 8  # from AMENITY
        assert result.priority_policy == 'less_usage_first'  # from TYPE
        assert result.priority_window_unit == 'month'  # from TYPE
        assert result.waitlist_mode == 'notify_and_confirm'  # from CONDOMINIUM
        assert result.approval_mode == 'auto'  # from CONDOMINIUM
        assert result.scope_level == 'AMENITY'
        assert result.source_policy_ids == [1, 2, 3]

    def test_resolve_with_no_policies(self):
        self.resolver._lookup_amenity_type = MagicMock(return_value='POOL')
        self.resolver._fetch_policies = MagicMock(return_value=[])
        self.resolver._enrich_from_amenity = MagicMock()

        result = self.resolver.resolve(condominium_id=1, amenity_id=10)

        assert result.eligibility_mode == 'all_residents'
        assert result.priority_policy == 'fifo'
        assert result.source_policy_ids == []

    def test_resolve_for_type(self):
        self.resolver._fetch_policies = MagicMock(return_value=[
            _make_row(id=1, scope_level='CONDOMINIUM', max_reservations_per_period=2),
            _make_row(id=2, scope_level='AMENITY_TYPE', amenity_type='POOL', max_guests=5),
        ])

        result = self.resolver.resolve_for_type(condominium_id=1, amenity_type='POOL')

        assert result.max_reservations_per_period == 2
        assert result.max_guests == 5
        assert result.source_policy_ids == [1, 2]
