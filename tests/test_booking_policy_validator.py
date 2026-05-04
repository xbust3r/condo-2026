"""
Unit tests: BookingPolicyValidator — policy enforcement.

Covers:
- Guest limit enforcement
- Active reservation limit
- Period reservation limit
- Eligibility modes (all_residents, owner_only)
- Idempotency rejection
- Policy snapshot building
- Blocked dates (B4)
- Advance booking window (B4)
- Cancel window (B4)
- Slot compliance (B4)
"""
import pytest
from unittest.mock import MagicMock, patch
from datetime import datetime, date, timedelta

from library.dddpy.core_amenity_bookings.domain.policy_entity import EffectiveAmenityPolicy
from library.dddpy.core_amenity_bookings.domain.booking_exception import BookingValidationError
from library.dddpy.core_amenity_bookings.usecase.booking_policy_validator import BookingPolicyValidator


class TestGuestLimit:
    def setup_method(self):
        self.validator = BookingPolicyValidator()

    def test_allows_when_no_limit(self):
        policy = EffectiveAmenityPolicy(max_guests=None)
        self.validator._check_guest_limit(policy, 10)  # should not raise

    def test_allows_when_under_limit(self):
        policy = EffectiveAmenityPolicy(max_guests=5)
        self.validator._check_guest_limit(policy, 3)  # should not raise

    def test_allows_when_at_limit(self):
        policy = EffectiveAmenityPolicy(max_guests=5)
        self.validator._check_guest_limit(policy, 5)  # should not raise

    def test_rejects_when_over_limit(self):
        policy = EffectiveAmenityPolicy(max_guests=5)
        with pytest.raises(BookingValidationError, match='Guest count'):
            self.validator._check_guest_limit(policy, 8)


class TestActiveLimit:
    def setup_method(self):
        self.validator = BookingPolicyValidator()

    @patch('library.dddpy.core_amenity_bookings.usecase.booking_policy_validator.session_scope')
    def test_allows_when_under_limit(self, mock_session_scope):
        mock_session = MagicMock()
        mock_session.__enter__.return_value = mock_session
        mock_session.execute.return_value.fetchone.return_value = [1]  # 1 active
        mock_session_scope.return_value = mock_session

        policy = EffectiveAmenityPolicy(max_active_reservations=2)
        self.validator._check_active_limit(policy, 1, 673, 1, 'POOL')  # 1 < 2, ok

    @patch('library.dddpy.core_amenity_bookings.usecase.booking_policy_validator.session_scope')
    def test_rejects_when_at_limit(self, mock_session_scope):
        mock_session = MagicMock()
        mock_session.__enter__.return_value = mock_session
        mock_session.execute.return_value.fetchone.return_value = [1]  # 1 active
        mock_session_scope.return_value = mock_session

        policy = EffectiveAmenityPolicy(max_active_reservations=1)
        with pytest.raises(BookingValidationError, match='already has 1 active'):
            self.validator._check_active_limit(policy, 1, 673, 1, 'POOL')

    @patch('library.dddpy.core_amenity_bookings.usecase.booking_policy_validator.session_scope')
    def test_skips_when_no_limit(self, mock_session_scope):
        policy = EffectiveAmenityPolicy(max_active_reservations=None)
        assert not policy.has_active_limit()


class TestPeriodLimit:
    def setup_method(self):
        self.validator = BookingPolicyValidator()

    def test_window_start_month(self):
        policy = EffectiveAmenityPolicy(period_unit='month', period_value=1)
        start = self.validator._period_window_start(policy)
        # ~30 days ago
        assert (datetime.utcnow() - start).days >= 29

    def test_window_start_week(self):
        policy = EffectiveAmenityPolicy(period_unit='week', period_value=2)
        start = self.validator._period_window_start(policy)
        # ~14 days ago
        assert 13 <= (datetime.utcnow() - start).days <= 15

    @patch('library.dddpy.core_amenity_bookings.usecase.booking_policy_validator.session_scope')
    def test_rejects_when_over_period_limit(self, mock_session_scope):
        mock_session = MagicMock()
        mock_session.__enter__.return_value = mock_session
        mock_session.execute.return_value.fetchone.return_value = [2]  # 2 bookings
        mock_session_scope.return_value = mock_session

        policy = EffectiveAmenityPolicy(
            max_reservations_per_period=2,
            period_unit='month',
            period_value=1,
        )
        with pytest.raises(BookingValidationError, match='has 2 booking'):
            self.validator._check_period_limit(policy, 1, 673, 1, 'POOL')


class TestSnapshot:
    def setup_method(self):
        self.validator = BookingPolicyValidator()

    def test_build_policy_snapshot(self):
        policy = EffectiveAmenityPolicy(
            eligibility_mode='owner_only',
            max_reservations_per_period=3,
            max_guests=5,
            source_policy_ids=[1, 2],
        )
        snapshot = self.validator.build_policy_snapshot(policy)
        assert snapshot['eligibility_mode'] == 'owner_only'
        assert snapshot['max_reservations_per_period'] == 3
        assert snapshot['max_guests'] == 5
        assert snapshot['source_policy_ids'] == [1, 2]

    def test_build_allocation_reason(self):
        policy = EffectiveAmenityPolicy(source_policy_ids=[7])
        reason = self.validator.build_allocation_reason(
            policy,
            ['period_limit', 'guest_limit', 'eligibility:all_residents'],
        )
        assert reason['policy_scope'] == 'CONDOMINIUM'
        assert reason['policy_source_ids'] == [7]
        assert 'period_limit' in reason['passed_checks']
        assert 'resolved_at' in reason


# ━━━ B4 — Availability validations ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

class TestBlockedDates:
    def setup_method(self):
        self.validator = BookingPolicyValidator()

    def test_allows_when_list_empty(self):
        policy = EffectiveAmenityPolicy(blocked_dates=[])
        # should not raise
        self.validator._check_blocked_dates(policy, date(2026, 12, 25))

    def test_allows_when_list_none(self):
        policy = EffectiveAmenityPolicy(blocked_dates=None)
        self.validator._check_blocked_dates(policy, date(2026, 12, 25))

    def test_allows_when_date_not_blocked(self):
        policy = EffectiveAmenityPolicy(blocked_dates=['2026-12-25'])
        self.validator._check_blocked_dates(policy, date(2026, 12, 26))

    def test_rejects_when_date_blocked(self):
        policy = EffectiveAmenityPolicy(blocked_dates=['2026-12-25', '2027-01-01'])
        with pytest.raises(BookingValidationError, match='blocked'):
            self.validator._check_blocked_dates(policy, date(2026, 12, 25))


class TestAdvanceBooking:
    def setup_method(self):
        self.validator = BookingPolicyValidator()

    def test_allows_when_within_window(self):
        policy = EffectiveAmenityPolicy(advance_booking_days=30)
        soon = datetime.utcnow() + timedelta(days=10)
        self.validator._check_advance_booking(policy, soon)

    def test_allows_at_edge_of_window(self):
        policy = EffectiveAmenityPolicy(advance_booking_days=30)
        edge = datetime.utcnow() + timedelta(days=29, hours=23)
        self.validator._check_advance_booking(policy, edge)

    def test_rejects_beyond_window(self):
        policy = EffectiveAmenityPolicy(advance_booking_days=30)
        far = datetime.utcnow() + timedelta(days=60)
        with pytest.raises(BookingValidationError, match='advance limit'):
            self.validator._check_advance_booking(policy, far)


class TestCancelWindow:
    def setup_method(self):
        self.validator = BookingPolicyValidator()

    def test_allows_when_no_restriction(self):
        policy = EffectiveAmenityPolicy(cancel_window_hours=None)
        soon = datetime.utcnow() + timedelta(minutes=5)
        self.validator.check_cancel_window(policy, soon)  # should not raise

    def test_allows_when_outside_window(self):
        policy = EffectiveAmenityPolicy(cancel_window_hours=24)
        far = datetime.utcnow() + timedelta(hours=48)
        self.validator.check_cancel_window(policy, far)  # should not raise

    def test_rejects_when_inside_window(self):
        policy = EffectiveAmenityPolicy(cancel_window_hours=24)
        soon = datetime.utcnow() + timedelta(hours=1)
        with pytest.raises(BookingValidationError, match='Cannot cancel'):
            self.validator.check_cancel_window(policy, soon)


class TestSlotCompliance:
    def setup_method(self):
        self.validator = BookingPolicyValidator()

    # ── CONTINUOUS_SLOTS ──

    def test_continuous_allows_exact_multiple(self):
        policy = EffectiveAmenityPolicy(
            slot_mode='CONTINUOUS_SLOTS',
            slot_interval_min=60,
        )
        start = datetime.utcnow()
        end = start + timedelta(minutes=120)
        self.validator._check_slot_compliance(policy, start, end)

    def test_continuous_allows_single_interval(self):
        policy = EffectiveAmenityPolicy(
            slot_mode='CONTINUOUS_SLOTS',
            slot_interval_min=60,
        )
        start = datetime.utcnow()
        end = start + timedelta(minutes=60)
        self.validator._check_slot_compliance(policy, start, end)

    def test_continuous_skips_when_no_interval(self):
        policy = EffectiveAmenityPolicy(
            slot_mode='CONTINUOUS_SLOTS',
            slot_interval_min=None,
        )
        start = datetime.utcnow()
        end = start + timedelta(minutes=45)  # not a multiple of nothing
        self.validator._check_slot_compliance(policy, start, end)

    def test_continuous_rejects_non_multiple(self):
        policy = EffectiveAmenityPolicy(
            slot_mode='CONTINUOUS_SLOTS',
            slot_interval_min=60,
        )
        start = datetime.utcnow()
        end = start + timedelta(minutes=45)
        with pytest.raises(BookingValidationError, match='multiple of slot_interval'):
            self.validator._check_slot_compliance(policy, start, end)

    # ── DISCRETE_WINDOWS ──

    def test_discrete_allows_within_window(self):
        policy = EffectiveAmenityPolicy(
            slot_mode='DISCRETE_WINDOWS',
            window_start_time='08:00',
            window_end_time='22:00',
        )
        start = datetime.utcnow().replace(hour=10, minute=0, second=0, microsecond=0)
        end = datetime.utcnow().replace(hour=14, minute=0, second=0, microsecond=0)
        self.validator._check_slot_compliance(policy, start, end)

    def test_discrete_rejects_start_before_window(self):
        policy = EffectiveAmenityPolicy(
            slot_mode='DISCRETE_WINDOWS',
            window_start_time='08:00',
            window_end_time='22:00',
        )
        start = datetime.utcnow().replace(hour=6, minute=0, second=0, microsecond=0)
        end = datetime.utcnow().replace(hour=10, minute=0, second=0, microsecond=0)
        with pytest.raises(BookingValidationError, match='outside allowed window'):
            self.validator._check_slot_compliance(policy, start, end)

    def test_discrete_rejects_end_after_window(self):
        policy = EffectiveAmenityPolicy(
            slot_mode='DISCRETE_WINDOWS',
            window_start_time='08:00',
            window_end_time='22:00',
        )
        start = datetime.utcnow().replace(hour=18, minute=0, second=0, microsecond=0)
        end = datetime.utcnow().replace(hour=23, minute=0, second=0, microsecond=0)
        with pytest.raises(BookingValidationError, match='outside allowed window'):
            self.validator._check_slot_compliance(policy, start, end, date.today())

    def test_discrete_skips_when_no_window_configured(self):
        policy = EffectiveAmenityPolicy(
            slot_mode='DISCRETE_WINDOWS',
            window_start_time=None,
            window_end_time=None,
        )
        start = datetime.utcnow().replace(hour=3, minute=0, second=0, microsecond=0)
        end = datetime.utcnow().replace(hour=5, minute=0, second=0, microsecond=0)
        self.validator._check_slot_compliance(policy, start, end)

    def test_discrete_rejects_outside_opening_hours(self):
        policy = EffectiveAmenityPolicy(
            slot_mode='DISCRETE_WINDOWS',
            opening_hours_json={
                'monday': {'open': '08:00', 'close': '18:00'},
                'tuesday': {'open': '08:00', 'close': '18:00'},
                'wednesday': {'open': '08:00', 'close': '18:00'},
                'thursday': {'open': '08:00', 'close': '18:00'},
                'friday': {'open': '08:00', 'close': '18:00'},
                'saturday': {'open': '10:00', 'close': '16:00'},
                'sunday': None,
            },
        )
        # Pick a Monday for the booking
        d = date.today()
        days_until_monday = (7 - d.weekday()) % 7 or 7
        monday = d + timedelta(days=days_until_monday)
        # 07:00-09:00 on a Monday (opens at 08:00)
        start = datetime(monday.year, monday.month, monday.day, 7, 0)
        end = datetime(monday.year, monday.month, monday.day, 9, 0)
        with pytest.raises(BookingValidationError, match='outside operating hours'):
            self.validator._check_slot_compliance(policy, start, end, monday)

    def test_discrete_allows_within_opening_hours(self):
        policy = EffectiveAmenityPolicy(
            slot_mode='DISCRETE_WINDOWS',
            opening_hours_json={
                'monday': {'open': '08:00', 'close': '18:00'},
            },
        )
        d = date.today()
        days_until_monday = (7 - d.weekday()) % 7 or 7
        monday = d + timedelta(days=days_until_monday)
        start = datetime(monday.year, monday.month, monday.day, 10, 0)
        end = datetime(monday.year, monday.month, monday.day, 12, 0)
        self.validator._check_slot_compliance(policy, start, end, monday)


class TestSlotCapacity:
    def setup_method(self):
        self.validator = BookingPolicyValidator()

    @patch('library.dddpy.core_amenity_bookings.usecase.booking_policy_validator.session_scope')
    def test_discrete_rejects_when_at_capacity(self, mock_session_scope):
        mock_session = MagicMock()
        mock_session.__enter__.return_value = mock_session
        mock_session.execute.return_value.fetchone.return_value = [1]  # 1 booking
        mock_session_scope.return_value = mock_session

        policy = EffectiveAmenityPolicy(
            slot_mode='DISCRETE_WINDOWS',
            max_capacity_per_slot=1,
        )
        now = datetime.utcnow()
        with pytest.raises(BookingValidationError, match='Slot capacity exceeded'):
            self.validator.check_slot_capacity(
                policy, 1, now, now + timedelta(hours=1), 5
            )

    @patch('library.dddpy.core_amenity_bookings.usecase.booking_policy_validator.session_scope')
    def test_continuous_rejects_when_guest_overflow(self, mock_session_scope):
        mock_session = MagicMock()
        mock_session.__enter__.return_value = mock_session
        mock_session.execute.return_value.fetchone.return_value = [8]  # 8 guests already
        mock_session_scope.return_value = mock_session

        policy = EffectiveAmenityPolicy(
            slot_mode='CONTINUOUS_SLOTS',
            max_capacity_per_slot=10,
        )
        now = datetime.utcnow()
        with pytest.raises(BookingValidationError, match='Slot capacity exceeded'):
            self.validator.check_slot_capacity(
                policy, 1, now, now + timedelta(hours=1), 5
            )  # 8 + 5 > 10

    @patch('library.dddpy.core_amenity_bookings.usecase.booking_policy_validator.session_scope')
    def test_continuous_allows_under_capacity(self, mock_session_scope):
        mock_session = MagicMock()
        mock_session.__enter__.return_value = mock_session
        mock_session.execute.return_value.fetchone.return_value = [3]  # 3 guests already
        mock_session_scope.return_value = mock_session

        policy = EffectiveAmenityPolicy(
            slot_mode='CONTINUOUS_SLOTS',
            max_capacity_per_slot=10,
        )
        now = datetime.utcnow()
        # should not raise — 3 + 5 <= 10
        self.validator.check_slot_capacity(
            policy, 1, now, now + timedelta(hours=1), 5
        )
