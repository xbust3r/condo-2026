"""
B8 Unit tests — observability use case contract + entity validation.

Covers:
- UsageLogEntity validation (event_type, source, required fields)
- UsageLogEntity.to_dict()
- UsageLogEntity.from_db_row()
- AmenityObservabilityUseCase contract (methods exist)
"""
import pytest
from datetime import datetime, date

from library.dddpy.core_amenity_bookings.domain.usage_log_entity import (
    UsageLogEntity,
    VALID_EVENT_TYPES,
    VALID_SOURCES,
)


class TestUsageLogEntity:
    def test_entity_creation_with_valid_data(self):
        entity = UsageLogEntity(
            id=1,
            uuid='test-uuid',
            booking_id=42,
            amenity_id=10,
            condominium_id=1,
            unit_id=673,
            owner_id=12,
            event_type='CHECK_IN',
            source='resident_app',
        )
        entity.validate()  # should not raise
        assert entity.booking_id == 42
        assert entity.event_type == 'CHECK_IN'

    def test_entity_rejects_invalid_event_type(self):
        entity = UsageLogEntity(
            booking_id=42, amenity_id=10, condominium_id=1,
            event_type='INVALID_TYPE',
        )
        with pytest.raises(ValueError, match='Invalid event_type'):
            entity.validate()

    def test_entity_rejects_invalid_source(self):
        entity = UsageLogEntity(
            booking_id=42, amenity_id=10, condominium_id=1,
            event_type='CHECK_IN', source='random_hacker',
        )
        with pytest.raises(ValueError, match='Invalid source'):
            entity.validate()

    def test_entity_rejects_missing_booking_id(self):
        entity = UsageLogEntity(
            booking_id=0, amenity_id=10, condominium_id=1,
            event_type='CHECK_IN', source='system',
        )
        with pytest.raises(ValueError, match='booking_id is required'):
            entity.validate()

    def test_entity_rejects_missing_amenity_id(self):
        entity = UsageLogEntity(
            booking_id=42, amenity_id=0, condominium_id=1,
            event_type='CHECK_IN', source='system',
        )
        with pytest.raises(ValueError, match='amenity_id is required'):
            entity.validate()

    def test_to_dict_includes_all_fields(self):
        now = datetime.utcnow()
        entity = UsageLogEntity(
            id=1, uuid='u1', booking_id=42, amenity_id=10,
            condominium_id=1, unit_id=673, owner_id=12,
            event_type='CHECK_IN', event_at=now, recorded_by=12,
            source='resident_app', notes='test', created_at=now,
        )
        d = entity.to_dict()
        assert d['event_type'] == 'CHECK_IN'
        assert d['booking_id'] == 42
        assert d['source'] == 'resident_app'
        assert d['notes'] == 'test'

    def test_from_db_row_populates_all_fields(self):
        now = datetime.utcnow()
        row = {
            'id': 1, 'uuid': 'u1', 'booking_id': 42, 'amenity_id': 10,
            'condominium_id': 1, 'unit_id': 673, 'owner_id': 12,
            'event_type': 'CHECK_OUT', 'event_at': now,
            'recorded_by': 13, 'source': 'admin_panel',
            'notes': 'done', 'event_context_json': {'key': 'val'},
            'created_at': now,
        }
        entity = UsageLogEntity.from_db_row(row)
        assert entity.event_type == 'CHECK_OUT'
        assert entity.unit_id == 673
        assert entity.event_context_json == {'key': 'val'}

    def test_all_valid_event_types_accepted(self):
        for et in VALID_EVENT_TYPES:
            entity = UsageLogEntity(
                booking_id=1, amenity_id=1, condominium_id=1,
                event_type=et, source='system',
            )
            entity.validate()  # should not raise

    def test_all_valid_sources_accepted(self):
        for src in VALID_SOURCES:
            entity = UsageLogEntity(
                booking_id=1, amenity_id=1, condominium_id=1,
                event_type='CHECK_IN', source=src,
            )
            entity.validate()  # should not raise


class TestAmenityObservabilityUseCase:
    """Contract tests for the observability use case methods."""

    def test_usecase_has_required_methods(self):
        from library.dddpy.core_amenity_bookings.usecase.amenity_observability_usecase import AmenityObservabilityUseCase
        uc = AmenityObservabilityUseCase()
        assert hasattr(uc, 'usage_timeline')
        assert hasattr(uc, 'operational_metrics')
        assert hasattr(uc, 'waitlist_metrics')
        assert hasattr(uc, 'combined_amenity_metrics')
        assert hasattr(uc, 'condominium_amenity_metrics')

    def test_operational_metrics_returns_expected_keys(self):
        """Verify the metrics dict structure (placeholder values when no data)."""
        from library.dddpy.core_amenity_bookings.usecase.amenity_observability_usecase import AmenityObservabilityUseCase
        uc = AmenityObservabilityUseCase()
        result = uc.operational_metrics(amenity_id=99999)
        assert 'total_check_ins' in result
        assert 'total_no_shows' in result
        assert 'total_tracked' in result
        assert 'check_in_rate' in result
        assert 'no_show_rate' in result

    def test_waitlist_metrics_returns_expected_keys(self):
        from library.dddpy.core_amenity_bookings.usecase.amenity_observability_usecase import AmenityObservabilityUseCase
        uc = AmenityObservabilityUseCase()
        result = uc.waitlist_metrics(amenity_id=99999)
        assert 'total_waitlisted' in result
        assert 'total_promoted' in result
        assert 'total_expired' in result
        assert 'conversion_rate' in result
        assert 'expiration_rate' in result

    def test_combined_amenity_metrics_has_all_sections(self):
        from library.dddpy.core_amenity_bookings.usecase.amenity_observability_usecase import AmenityObservabilityUseCase
        uc = AmenityObservabilityUseCase()
        result = uc.combined_amenity_metrics(amenity_id=99999)
        assert 'operational' in result
        assert 'waitlist' in result
        assert 'rejection_distribution' in result
        assert 'conversion_detail' in result


class TestAmenityUsageUseCase:
    """Contract tests for the usage use case methods."""

    def test_usecase_has_required_methods(self):
        from library.dddpy.core_amenity_bookings.usecase.amenity_usage_usecase import AmenityUsageUseCase
        uc = AmenityUsageUseCase()
        assert hasattr(uc, 'check_in')
        assert hasattr(uc, 'check_out')
        assert hasattr(uc, 'mark_no_show')
        assert hasattr(uc, 'get_booking_usage')
