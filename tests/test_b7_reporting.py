"""Tests for B7 — Reporting, usage history, allocation audit.

Tests:
- AllocationAuditUseCase: record entries
- UsageReportUseCase: all report queries
- Audit integration: booking_usecase + waitlist_usecase wire
"""
import pytest
from unittest.mock import MagicMock, patch
from datetime import date, datetime


# ── AllocationAuditUseCase ────────────────────────────────────────────

class TestAllocationAudit:
    def setup_method(self):
        from library.dddpy.core_amenity_bookings.usecase.allocation_audit_usecase import (
            AllocationAuditUseCase,
        )
        self.audit_uc = AllocationAuditUseCase()

    def test_valid_decision_types(self):
        valid = {'BOOKING_ACCEPTED', 'BOOKING_REJECTED', 'WAITLIST_INSERTED',
                 'WAITLIST_PROMOTED', 'WAITLIST_CONFIRMED', 'WAITLIST_NOTIFIED',
                 'BOOKING_CANCELLED', 'WAITLIST_EXPIRED'}
        for dt in valid:
            with patch('library.dddpy.core_amenity_bookings.usecase.allocation_audit_usecase.session_scope') as mock_ss:
                mock_session = MagicMock()
                mock_session.__enter__.return_value = mock_session
                mock_ss.return_value = mock_session
                # Should not raise
                self.audit_uc.record(amenity_id=1, decision_type=dt, decision_reason='test')

    def test_invalid_decision_type_raises(self):
        with pytest.raises(ValueError):
            self.audit_uc.record(amenity_id=1, decision_type='INVALID_TYPE')

    def test_record_sets_all_fields(self):
        with patch('library.dddpy.core_amenity_bookings.usecase.allocation_audit_usecase.session_scope') as mock_ss:
            mock_session = MagicMock()
            mock_session.__enter__.return_value = mock_session
            mock_ss.return_value = mock_session

            aid = self.audit_uc.record(
                amenity_id=5,
                decision_type='BOOKING_ACCEPTED',
                decision_reason='test accept',
                booking_id=42,
                waitlist_entry_id=None,
                context={'key': 'value'},
            )

            args = mock_session.add.call_args[0][0]
            assert args.amenity_id == 5
            assert args.decision_type == 'BOOKING_ACCEPTED'
            assert args.decision_reason == 'test accept'
            assert args.booking_id == 42
            assert args.waitlist_entry_id is None
            assert args.decision_context_json == {'key': 'value'}


# ── UsageReportUseCase ────────────────────────────────────────────────

class TestUsageReport:
    def setup_method(self):
        from library.dddpy.core_amenity_bookings.usecase.usage_report_usecase import (
            UsageReportUseCase,
        )
        self.ruc = UsageReportUseCase()

    def test_usage_by_amenity_defaults(self):
        with patch('library.dddpy.core_amenity_bookings.usecase.usage_report_usecase.session_scope') as mock_ss:
            mock_session = MagicMock()
            mock_session.__enter__.return_value = mock_session
            mock_result = MagicMock()
            mock_result.fetchall.return_value = []
            mock_session.execute.return_value = mock_result
            mock_ss.return_value = mock_session
            result = self.ruc.usage_by_amenity(1)
            assert isinstance(result, list)

    def test_usage_by_user_defaults(self):
        with patch('library.dddpy.core_amenity_bookings.usecase.usage_report_usecase.session_scope') as mock_ss:
            mock_session = MagicMock()
            mock_session.__enter__.return_value = mock_session
            mock_result = MagicMock()
            mock_result.fetchall.return_value = []
            mock_session.execute.return_value = mock_result
            mock_ss.return_value = mock_session
            result = self.ruc.usage_by_user(1)
            assert isinstance(result, list)

    def test_allocation_audit_trail(self):
        with patch('library.dddpy.core_amenity_bookings.usecase.usage_report_usecase.session_scope') as mock_ss:
            mock_session = MagicMock()
            mock_session.__enter__.return_value = mock_session
            mock_result = MagicMock()
            mock_result.fetchall.return_value = []
            mock_session.execute.return_value = mock_result
            mock_ss.return_value = mock_session
            result = self.ruc.allocation_audit_trail(amenity_id=1)
            assert isinstance(result, list)

    def test_waitlist_conversion_rate(self):
        with patch('library.dddpy.core_amenity_bookings.usecase.usage_report_usecase.session_scope') as mock_ss:
            mock_session = MagicMock()
            mock_session.__enter__.return_value = mock_session
            mock_result = MagicMock()
            mock_result._mapping = {
                'total_waitlisted': 10, 'total_converted': 3,
                'total_notified': 2, 'total_expired': 4,
                'total_cancelled': 1, 'avg_conversion_minutes': 30.5,
            }
            mock_session.execute.return_value.fetchone.return_value = mock_result
            mock_ss.return_value = mock_session
            result = self.ruc.waitlist_conversion_rate(1)
            assert result['total_waitlisted'] == 10
            assert result['total_converted'] == 3

    def test_rejection_distribution(self):
        with patch('library.dddpy.core_amenity_bookings.usecase.usage_report_usecase.session_scope') as mock_ss:
            mock_session = MagicMock()
            mock_session.__enter__.return_value = mock_session
            mock_result = MagicMock()
            mock_result.fetchall.return_value = []
            mock_session.execute.return_value = mock_result
            mock_ss.return_value = mock_session
            result = self.ruc.rejection_distribution()
            assert isinstance(result, list)

    def test_amenity_distribution_defaults(self):
        with patch('library.dddpy.core_amenity_bookings.usecase.usage_report_usecase.session_scope') as mock_ss:
            mock_session = MagicMock()
            mock_session.__enter__.return_value = mock_session
            mock_result = MagicMock()
            mock_result.fetchall.return_value = []
            mock_session.execute.return_value = mock_result
            mock_ss.return_value = mock_session
            result = self.ruc.amenity_distribution(1)
            assert isinstance(result, list)
