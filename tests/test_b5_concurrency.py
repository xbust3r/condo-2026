"""
Unit tests: B5 — Concurrency hardening, idempotency, waitlist base.

Covers:
- MySQL named lock acquisition / release
- Idempotent retry via find_by_idempotency_key (Phase 0, before validation)
- Waitlist model and to_dict
"""
import pytest
from unittest.mock import MagicMock, patch
from datetime import datetime, date, timedelta

from library.dddpy.core_amenity_bookings.domain.booking_exception import BookingValidationError
from library.dddpy.core_amenity_bookings.usecase.booking_usecase import BookingUseCase
from library.dddpy.core_amenity_bookings.infrastructure.dbwaitlist import DBWaitlistEntry


class TestNamedLock:
    """Lock acquisition and release on the amenity."""

    @patch('library.dddpy.core_amenity_bookings.usecase.booking_usecase.session_scope')
    def test_acquire_lock_success(self, mock_session_scope):
        mock_session = MagicMock()
        mock_session.__enter__.return_value = mock_session
        mock_session.execute.return_value.fetchone.return_value = [1]
        mock_session_scope.return_value = mock_session

        uc = BookingUseCase()
        uc._acquire_amenity_lock('booking_amenity_42')
        assert uc._lock_session is not None

    @patch('library.dddpy.core_amenity_bookings.usecase.booking_usecase.session_scope')
    def test_acquire_lock_timeout_raises(self, mock_session_scope):
        mock_session = MagicMock()
        mock_session.__enter__.return_value = mock_session
        mock_session.execute.return_value.fetchone.return_value = [0]
        mock_session_scope.return_value = mock_session

        uc = BookingUseCase()
        with pytest.raises(BookingValidationError, match='Could not acquire lock'):
            uc._acquire_amenity_lock('booking_amenity_42')
        assert uc._lock_session is None

    @patch('library.dddpy.core_amenity_bookings.usecase.booking_usecase.session_scope')
    def test_release_lock_cleans_up(self, mock_session_scope):
        mock_session = MagicMock()
        mock_session.__enter__.return_value = mock_session
        mock_session.execute.return_value.fetchone.return_value = [1]
        mock_session_scope.return_value = mock_session

        uc = BookingUseCase()
        uc._acquire_amenity_lock('booking_amenity_42')
        assert uc._lock_session is not None
        uc._release_amenity_lock('booking_amenity_42')
        assert uc._lock_session is None


class TestIdempotentRetry:
    """find_by_idempotency_key runs in Phase 0 — before any lock or validation."""

    def setup_method(self):
        self.uc = BookingUseCase()

    def test_idempotent_retry_returns_existing(self):
        """Same idempotency_key returns the existing booking, skipping all validation."""
        mock_query_repo = MagicMock()
        mock_query_repo.find_by_idempotency_key.return_value = MagicMock(
            id=42, to_dict=lambda: {'id': 42, 'status': 'draft'}
        )
        self.uc._query_repo = mock_query_repo

        result = self.uc.create(
            condominium_id=1, building_id=1, amenity_id=1,
            unit_id=673, owner_id=12,
            booking_date=date.today() + timedelta(days=5),
            start_at=datetime.utcnow() + timedelta(days=5, hours=10),
            end_at=datetime.utcnow() + timedelta(days=5, hours=11),
            guest_count=1,
            idempotency_key='test-key-b5',
        )
        assert result.data['id'] == 42
        assert 'idempotent retry' in result.message.lower()

    def test_no_idempotency_key_skips_check(self):
        """Without idempotency_key, the repo method is never called."""
        mock_query_repo = MagicMock()
        mock_query_repo.find_by_idempotency_key.return_value = None
        self.uc._query_repo = mock_query_repo

        with pytest.raises(Exception):
            self.uc.create(
                condominium_id=1, building_id=1, amenity_id=9999,
                unit_id=673, owner_id=12,
                booking_date=date.today(),
                start_at=datetime.utcnow(),
                end_at=datetime.utcnow() + timedelta(hours=1),
                guest_count=1,
            )
        mock_query_repo.find_by_idempotency_key.assert_not_called()


class TestWaitlistBase:
    """core_amenity_waitlist model and table structure."""

    def test_table_name(self):
        assert DBWaitlistEntry.__tablename__ == 'core_amenity_waitlist'

    def test_status_column_default(self):
        """Default is 'WAITING' (Python-level Column default, DB server_default in migration)."""
        c = DBWaitlistEntry.__table__.c.status
        # SQLAlchemy Column uses default='WAITING' (Python-level), migration uses server_default
        assert c.default.arg == 'WAITING'

    def test_guest_count_column_default(self):
        """Python-level default is 1."""
        c = DBWaitlistEntry.__table__.c.guest_count
        assert c.default is not None
        assert c.default.arg == 1

    def test_to_dict_has_required_keys(self):
        entry = DBWaitlistEntry(
            uuid='abc-123',
            amenity_id=5,
            unit_id=10,
            user_id=20,
            booking_date=date(2026, 12, 25),
            requested_start_at=datetime(2026, 12, 25, 10, 0),
            requested_end_at=datetime(2026, 12, 25, 12, 0),
            guest_count=4,
            status='WAITING',
            idempotency_key='wl-key-1',
            notes='test waitlist entry',
            created_at=datetime(2026, 5, 4, 0, 0),
        )
        d = entry.to_dict()
        assert d['uuid'] == 'abc-123'
        assert d['amenity_id'] == 5
        assert d['booking_date'] == '2026-12-25'
        assert d['guest_count'] == 4
        assert d['status'] == 'WAITING'
        assert d['idempotency_key'] == 'wl-key-1'
        assert d['notes'] == 'test waitlist entry'

    def test_to_dict_handles_nullables(self):
        entry = DBWaitlistEntry(
            uuid='def-456',
            amenity_id=1,
            unit_id=1,
            user_id=1,
            booking_date=date.today(),
            requested_start_at=datetime.utcnow(),
            requested_end_at=datetime.utcnow(),
            created_at=datetime.utcnow(),
        )
        d = entry.to_dict()
        assert d['priority_score_snapshot'] is None
        assert d['priority_reason_json'] is None
        assert d['effective_policy_snapshot_json'] is None
        assert d['expires_at'] is None
        assert d['notified_at'] is None
        assert d['converted_booking_id'] is None
        assert d['updated_at'] is None
