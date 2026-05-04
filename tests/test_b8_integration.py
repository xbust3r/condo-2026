"""
B8 Integration tests — usage logs + observability.

Tests:
- CHECK_IN for confirmed booking
- CHECK_IN → CHECK_OUT happy path
- NO_SHOW for confirmed booking without CHECK_IN
- Blocked: double CHECK_IN, CHECK_OUT without CHECK_IN, NO_SHOW with CHECK_IN
- Usage timeline retrieval
- Allocation audit trail filtering
- Operational + waitlist metrics
- Condominium-level amenity metrics
"""
import pytest
import uuid as _uuid
from datetime import date, datetime, timedelta
from library.dddpy.shared.mysql.session_manager import session_scope
from sqlalchemy import text as sa_text


def _clean():
    """Nuke all test-created data (B7 style + usage logs)."""
    with session_scope() as s:
        for stmt in [
            "DELETE FROM core_amenity_usage_logs",
            "DELETE FROM core_amenity_allocation_audit",
            "DELETE FROM core_amenity_waitlist",
            "DELETE FROM core_amenity_bookings WHERE condominium_id=1",
            "DELETE FROM core_amenity_availability_rules WHERE amenity_id IS NOT NULL",
            "DELETE FROM core_amenity_policies",
            "DELETE FROM core_amenities WHERE uuid LIKE 'b8-int-%'",
            "DELETE FROM core_amenities WHERE uuid LIKE 'b7-int-%'",
            "DELETE FROM core_amenities WHERE uuid LIKE '%debug%'",
            "DELETE FROM core_unit_ownerships WHERE unit_id IN (673,674) AND created_at IS NOT NULL",
        ]:
            s.execute(sa_text(stmt))


def _seed_condominium():
    """Ensure condominium id=1, building id=1, units 673/674, and user 12 exist."""
    with session_scope() as s:
        s.execute(sa_text("INSERT IGNORE INTO users (id, uuid, email, status, token_version, created_at, updated_at) VALUES (12, UUID(), 'test.user@condo.test', 'active', 1, NOW(), NOW())"))
        s.execute(sa_text("INSERT IGNORE INTO core_condominiums (id, uuid, name, code, status, created_at, updated_at) VALUES (1, UUID(), 'Test Condominium', 'TC001', 1, NOW(), NOW())"))
        s.execute(sa_text("INSERT IGNORE INTO core_buildings (id, uuid, condominium_id, name, code, status, created_at, updated_at) VALUES (1, UUID(), 1, 'Test Building', 'TB001', 1, NOW(), NOW())"))
        s.execute(sa_text("INSERT IGNORE INTO core_units (id, uuid, building_id, name, code, unit_number, occupancy_status, status, created_at, updated_at) VALUES (673, UUID(), 1, 'Test Unit 673', 'U673', '673', 'vacant', 1, NOW(), NOW())"))
        s.execute(sa_text("INSERT IGNORE INTO core_units (id, uuid, building_id, name, code, unit_number, occupancy_status, status, created_at, updated_at) VALUES (674, UUID(), 1, 'Test Unit 674', 'U674', '674', 'vacant', 1, NOW(), NOW())"))


def _seed_ownership():
    with session_scope() as s:
        s.execute(sa_text("INSERT IGNORE INTO core_unit_ownerships (unit_id, user_id, ownership_percentage, created_at) VALUES (673, 12, 100.00, NOW())"))
        s.execute(sa_text("INSERT IGNORE INTO core_unit_ownerships (unit_id, user_id, ownership_percentage, created_at) VALUES (674, 12, 100.00, NOW())"))


def _create_amenity(max_capacity_per_slot=5, waitlist_mode=None):
    uid = str(_uuid.uuid4())[:8]
    with session_scope() as s:
        s.execute(sa_text(
            "INSERT INTO core_amenities (uuid, condominium_id, building_id, name, amenity_type, scope, max_capacity, booking_duration_min, requires_approval, is_reservable, status) VALUES (:uid, 1, 1, 'B8 Pool', 'POOL', 'CONDOMINIUM', 20, 120, 0, 1, 'active')"
        ), {'uid': f'b8-int-{uid}'})
        aid = s.execute(sa_text("SELECT LAST_INSERT_ID()")).fetchone()[0]
        s.execute(sa_text(
            "INSERT INTO core_amenity_availability_rules (amenity_id, slot_mode, slot_interval_min, max_capacity_per_slot, advance_booking_days, cancel_window_hours, created_at) VALUES (:aid, 'CONTINUOUS_SLOTS', 60, :cap, 30, 24, NOW())"
        ), {'aid': aid, 'cap': max_capacity_per_slot})
        s.execute(sa_text(
            "INSERT INTO core_amenity_policies (condominium_id, scope_level, max_active_reservations, max_guests, waitlist_mode, eligibility_mode, approval_mode, priority_policy, created_at) VALUES (1, 'CONDOMINIUM', 10, 20, :wm, 'all_residents', 'auto', 'fifo', NOW())"
        ), {'wm': waitlist_mode})
    return aid


def _create_confirmed_booking(aid, unit_id, hour, guest_count=1):
    from library.dddpy.core_amenity_bookings.usecase.booking_usecase import BookingUseCase
    d = date.today() + timedelta(days=14)
    uc = BookingUseCase()
    r = uc.create(
        condominium_id=1, building_id=1, amenity_id=aid, unit_id=unit_id, owner_id=12,
        booking_date=d, start_at=datetime(d.year,d.month,d.day,hour,0),
        end_at=datetime(d.year,d.month,d.day,hour+1,0), guest_count=guest_count)
    uc.confirm(r.data['id'])
    return r.data['id']


class TestB8UsageLogs:
    @classmethod
    def setup_class(cls):
        from library.dddpy.core_amenity_bookings.usecase.amenity_usage_usecase import AmenityUsageUseCase
        cls.usage_uc = AmenityUsageUseCase()

    def setup_method(self):
        _clean()
        _seed_condominium()
        _seed_ownership()

    # ── G1: CHECK_IN happy path ──────────────────────────────────────

    def test_check_in_happy_path(self):
        aid = _create_amenity(max_capacity_per_slot=5)
        bid = _create_confirmed_booking(aid, 673, 10)
        result = self.usage_uc.check_in(booking_id=bid, recorded_by=12, notes="Arrived on time")
        assert result['event_type'] == 'CHECK_IN'
        assert result['booking_id'] == bid
        assert result['notes'] == 'Arrived on time'

    # ── G2: CHECK_OUT after CHECK_IN ─────────────────────────────────

    def test_check_out_after_check_in(self):
        aid = _create_amenity(max_capacity_per_slot=5)
        bid = _create_confirmed_booking(aid, 673, 10)
        self.usage_uc.check_in(booking_id=bid, recorded_by=12)
        result = self.usage_uc.check_out(booking_id=bid, recorded_by=12, notes="Left clean")
        assert result['event_type'] == 'CHECK_OUT'
        assert result['booking_id'] == bid

    # ── G3: NO_SHOW for confirmed booking without CHECK_IN ────────────

    def test_no_show_for_confirmed_booking(self):
        aid = _create_amenity(max_capacity_per_slot=5)
        bid = _create_confirmed_booking(aid, 673, 10)
        result = self.usage_uc.mark_no_show(booking_id=bid, recorded_by=12, notes="Never came")
        assert result['event_type'] == 'NO_SHOW'
        assert result['booking_id'] == bid

    # ── G4: Double CHECK_IN blocked ──────────────────────────────────

    def test_double_check_in_blocked(self):
        aid = _create_amenity(max_capacity_per_slot=5)
        bid = _create_confirmed_booking(aid, 673, 10)
        self.usage_uc.check_in(booking_id=bid, recorded_by=12)
        with pytest.raises(ValueError, match="already has an active CHECK_IN"):
            self.usage_uc.check_in(booking_id=bid, recorded_by=12)

    # ── G5: CHECK_OUT without CHECK_IN blocked ───────────────────────

    def test_check_out_without_check_in_blocked(self):
        aid = _create_amenity(max_capacity_per_slot=5)
        bid = _create_confirmed_booking(aid, 673, 10)
        with pytest.raises(ValueError, match="no CHECK_IN found"):
            self.usage_uc.check_out(booking_id=bid, recorded_by=12)

    # ── G6: NO_SHOW blocked after CHECK_IN ───────────────────────────

    def test_no_show_blocked_after_check_in(self):
        aid = _create_amenity(max_capacity_per_slot=5)
        bid = _create_confirmed_booking(aid, 673, 10)
        self.usage_uc.check_in(booking_id=bid, recorded_by=12)
        with pytest.raises(ValueError, match="already has CHECK_IN"):
            self.usage_uc.mark_no_show(booking_id=bid, recorded_by=12)

    # ── G7: Usage timeline retrieval ─────────────────────────────────

    def test_usage_timeline_retrieval(self):
        aid = _create_amenity(max_capacity_per_slot=5)
        bid = _create_confirmed_booking(aid, 673, 10)
        self.usage_uc.check_in(booking_id=bid, recorded_by=12)
        self.usage_uc.check_out(booking_id=bid, recorded_by=12)
        timeline = self.usage_uc.get_booking_usage(bid)
        assert len(timeline) == 2
        types = [t['event_type'] for t in timeline]
        assert types == ['CHECK_IN', 'CHECK_OUT']


class TestB8Observability:
    @classmethod
    def setup_class(cls):
        from library.dddpy.core_amenity_bookings.usecase.amenity_usage_usecase import AmenityUsageUseCase
        from library.dddpy.core_amenity_bookings.usecase.amenity_observability_usecase import AmenityObservabilityUseCase
        from library.dddpy.core_amenity_bookings.usecase.usage_report_usecase import UsageReportUseCase
        cls.usage_uc = AmenityUsageUseCase()
        cls.obs_uc = AmenityObservabilityUseCase()
        cls.ruc = UsageReportUseCase()
        cls.d = date.today() + timedelta(days=14)

    def setup_method(self):
        _clean()
        _seed_condominium()
        _seed_ownership()

    # ── G8: Allocation audit filtering ───────────────────────────────

    def test_allocation_audit_filtering(self):
        aid = _create_amenity(max_capacity_per_slot=1, waitlist_mode=None)
        from library.dddpy.core_amenity_bookings.domain.booking_exception import BookingValidationError
        bid = _create_confirmed_booking(aid, 673, 10)
        # Second booking on same slot should be rejected (capacity=1)
        try:
            _create_confirmed_booking(aid, 674, 10)
        except BookingValidationError:
            pass  # Expected

        trail = self.ruc.allocation_audit_trail(amenity_id=aid, limit=20)
        assert len(trail) >= 2, f"Expected >=2 audit entries, got {len(trail)}: {[t['decision_type'] for t in trail]}"
        types = [t['decision_type'] for t in trail]
        assert 'BOOKING_ACCEPTED' in types
        assert 'BOOKING_REJECTED' in types

    # ── G9: Operational metrics ──────────────────────────────────────

    def test_operational_metrics_with_data(self):
        aid = _create_amenity(max_capacity_per_slot=5)
        bid = _create_confirmed_booking(aid, 673, 10)
        self.usage_uc.check_in(booking_id=bid, recorded_by=12)
        self.usage_uc.check_out(booking_id=bid, recorded_by=12)

        today = date.today()
        metrics = self.obs_uc.operational_metrics(
            amenity_id=aid,
            from_date=today - timedelta(1),
            to_date=today + timedelta(1),
        )
        assert metrics['total_check_ins'] >= 1
        assert metrics['check_in_rate'] >= 0.9

    # ── G10: Combined amenity metrics snapshot ────────────────────────

    def test_combined_amenity_metrics(self):
        aid = _create_amenity(max_capacity_per_slot=5)
        bid = _create_confirmed_booking(aid, 673, 10)
        self.usage_uc.check_in(booking_id=bid, recorded_by=12)

        today = date.today()
        snapshot = self.obs_uc.combined_amenity_metrics(
            amenity_id=aid,
            from_date=today - timedelta(1),
            to_date=today + timedelta(1),
        )
        assert 'operational' in snapshot
        assert 'waitlist' in snapshot
        assert 'rejection_distribution' in snapshot
        assert snapshot['operational']['total_check_ins'] >= 1

    # ── G11: Condominium-level metrics ───────────────────────────────

    def test_condominium_amenity_metrics(self):
        aid = _create_amenity(max_capacity_per_slot=5)
        _create_confirmed_booking(aid, 673, 10)

        metrics = self.obs_uc.condominium_amenity_metrics(
            condominium_id=1,
            from_date=self.d - timedelta(1),
            to_date=self.d + timedelta(1),
        )
        our = [m for m in metrics if m['amenity_id'] == aid]
        assert len(our) >= 1
        assert our[0]['total_bookings'] >= 1

    # ── G12: Usage timeline by amenity ───────────────────────────────

    def test_usage_timeline_by_amenity(self):
        aid = _create_amenity(max_capacity_per_slot=5)
        bid = _create_confirmed_booking(aid, 673, 10)
        self.usage_uc.check_in(booking_id=bid, recorded_by=12)

        today = date.today()
        timeline = self.obs_uc.usage_timeline(
            amenity_id=aid,
            from_date=today - timedelta(1),
            to_date=today + timedelta(1),
        )
        assert len(timeline) >= 1
        assert timeline[0]['event_type'] == 'CHECK_IN'

    # ── G13: Waitlist metrics ────────────────────────────────────────

    def test_waitlist_metrics(self):
        aid = _create_amenity(max_capacity_per_slot=1, waitlist_mode='auto_confirm')
        bid = _create_confirmed_booking(aid, 673, 10)

        from library.dddpy.core_amenity_bookings.usecase.booking_usecase import BookingUseCase
        uc = BookingUseCase()
        # Over-capacity triggers waitlist
        r = uc.create(
            condominium_id=1, building_id=1, amenity_id=aid,
            unit_id=674, owner_id=12, booking_date=self.d,
            start_at=datetime(self.d.year,self.d.month,self.d.day,10,0),
            end_at=datetime(self.d.year,self.d.month,self.d.day,11,0),
            guest_count=1)
        assert r.data.get('waitlist_entry_id'), f"Expected waitlist, got {r.data}"

        wm = self.obs_uc.waitlist_metrics(
            amenity_id=aid,
            from_date=self.d - timedelta(1),
            to_date=self.d + timedelta(1),
        )
        assert wm['total_waitlisted'] >= 1
