"""
B7 Integration tests — real DB, no mocks.

Tests:
- BOOKING_REJECTED audit entries for capacity full (no waitlist)
- Audit trail after: create booking, reject, waitlist+
- All 6 UsageReportUseCase methods with real data
"""
import pytest
import uuid as _uuid
from datetime import date, datetime, timedelta
from library.dddpy.shared.mysql.session_manager import session_scope
from sqlalchemy import text as sa_text


def _clean():
    """Nuke all test-created data."""
    with session_scope() as s:
        for stmt in [
            "DELETE FROM core_amenity_allocation_audit",
            "DELETE FROM core_amenity_waitlist",
            "DELETE FROM core_amenity_bookings WHERE condominium_id=1",
            "DELETE FROM core_amenity_availability_rules WHERE amenity_id IS NOT NULL",
            "DELETE FROM core_amenity_policies",
            "DELETE FROM core_amenities WHERE uuid LIKE 'b7-int-%'",
            "DELETE FROM core_amenities WHERE uuid LIKE '%debug%'",
            "DELETE FROM core_unit_ownerships WHERE unit_id IN (673,674) AND created_at IS NOT NULL",
        ]:
            s.execute(sa_text(stmt))


def _seed_condominium():
    """Ensure condominium id=1, building id=1, units 673/674, and user 12 exist in test DB."""
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


def _create_amenity(max_capacity_per_slot=2, waitlist_mode=None):
    uid = str(_uuid.uuid4())[:8]
    with session_scope() as s:
        s.execute(sa_text(
            "INSERT INTO core_amenities (uuid, condominium_id, building_id, name, amenity_type, scope, max_capacity, booking_duration_min, requires_approval, is_reservable, status) VALUES (:uid, 1, 1, 'SUM Int', 'SUM', 'CONDOMINIUM', 20, 120, 0, 1, 'active')"
        ), {'uid': f'b7-int-{uid}'})
        aid = s.execute(sa_text("SELECT LAST_INSERT_ID()")).fetchone()[0]
        s.execute(sa_text(
            "INSERT INTO core_amenity_availability_rules (amenity_id, slot_mode, slot_interval_min, max_capacity_per_slot, advance_booking_days, cancel_window_hours, created_at) VALUES (:aid, 'CONTINUOUS_SLOTS', 60, :cap, 30, 24, NOW())"
        ), {'aid': aid, 'cap': max_capacity_per_slot})
        s.execute(sa_text(
            "INSERT INTO core_amenity_policies (condominium_id, scope_level, max_active_reservations, max_guests, waitlist_mode, eligibility_mode, approval_mode, priority_policy, created_at) VALUES (1, 'CONDOMINIUM', 10, 20, :wm, 'all_residents', 'auto', 'fifo', NOW())"
        ), {'wm': waitlist_mode})
    return aid


class TestB7Integration:
    @classmethod
    def setup_class(cls):
        from library.dddpy.core_amenity_bookings.usecase.booking_usecase import BookingUseCase
        from library.dddpy.core_amenity_bookings.usecase.waitlist_usecase import WaitlistUseCase
        from library.dddpy.core_amenity_bookings.usecase.usage_report_usecase import UsageReportUseCase
        cls.uc = BookingUseCase(); cls.wl_uc = WaitlistUseCase(); cls.ruc = UsageReportUseCase()
        cls.d = date.today() + timedelta(days=10)

    def setup_method(self):
        _clean()
        _seed_condominium()
        _seed_ownership()

    def _book(self, aid, unit_id, hour, guest_count=1):
        d = self.d
        return self.uc.create(
            condominium_id=1, building_id=1, amenity_id=aid, unit_id=unit_id, owner_id=12,
            booking_date=d, start_at=datetime(d.year,d.month,d.day,hour,0),
            end_at=datetime(d.year,d.month,d.day,hour+1,0), guest_count=guest_count)

    def _confirm_bookings(self, aid):
        with session_scope() as s:
            s.execute(sa_text("UPDATE core_amenity_bookings SET status='confirmed' WHERE amenity_id=:aid"), {'aid': aid})

    # ── G1: BOOKING_REJECTED audit ───────────────────────────────────

    def test_rejected_audit_capacity_full(self):
        aid = _create_amenity(max_capacity_per_slot=1, waitlist_mode=None)
        self._book(aid, 673, 10)
        from library.dddpy.core_amenity_bookings.domain.booking_exception import BookingValidationError
        with pytest.raises(BookingValidationError):
            self._book(aid, 674, 10)
        trail = self.ruc.allocation_audit_trail(amenity_id=aid, limit=10)
        rejected = [t for t in trail if t['decision_type'] == 'BOOKING_REJECTED']
        accepted = [t for t in trail if t['decision_type'] == 'BOOKING_ACCEPTED']
        assert len(accepted) == 1
        assert len(rejected) == 1, f"Missing BOOKING_REJECTED: {[t['decision_type'] for t in trail]}"

    # ── G2: Rejection distribution ──────────────────────────────────

    def test_rejection_distribution_not_empty(self):
        aid = _create_amenity(max_capacity_per_slot=1, waitlist_mode=None)
        self._book(aid, 673, 10)
        from library.dddpy.core_amenity_bookings.domain.booking_exception import BookingValidationError
        with pytest.raises(BookingValidationError):
            self._book(aid, 674, 10)
        rj = self.ruc.rejection_distribution()
        assert len(rj) >= 1
        assert rj[0]['count'] == 1

    # ── G3: Usage by amenity ────────────────────────────────────────

    def test_usage_by_amenity_with_bookings(self):
        aid = _create_amenity(max_capacity_per_slot=5)
        self._book(aid, 673, 10, guest_count=3)
        self._confirm_bookings(aid)
        usage = self.ruc.usage_by_amenity(aid, from_date=self.d-timedelta(1), to_date=self.d+timedelta(1))
        assert sum(u['total_bookings'] for u in usage) >= 1
        assert sum(u['total_guests'] for u in usage) >= 3

    # ── G4: Usage by user ──────────────────────────────────────────

    def test_usage_by_user_with_bookings(self):
        aid = _create_amenity(max_capacity_per_slot=5)
        self._book(aid, 673, 10, guest_count=2)
        self._confirm_bookings(aid)
        by_user = self.ruc.usage_by_user(1, from_date=self.d-timedelta(1), to_date=self.d+timedelta(1))
        assert len(by_user) >= 1
        assert by_user[0]['total_bookings'] == 1

    # ── G5: Audit trail end-to-end ──────────────────────────────────

    def test_audit_trail_waitlist_flow(self):
        aid = _create_amenity(max_capacity_per_slot=1, waitlist_mode='notify_and_confirm')
        r1 = self._book(aid, 673, 10); self.uc.cancel(r1.data['id'], reason='test')
        r2 = self._book(aid, 674, 10)
        r3 = self._book(aid, 673, 10, guest_count=1)
        assert r3.data.get('waitlist_entry_id')
        self.uc.cancel(r2.data['id'], reason='test')
        self.wl_uc.promote(aid, self.d, waitlist_mode='notify_and_confirm', condominium_id=1)
        trail = self.ruc.allocation_audit_trail(amenity_id=aid, limit=20)
        types = [t['decision_type'] for t in trail]
        assert 'BOOKING_ACCEPTED' in types and 'WAITLIST_NOTIFIED' in types

    # ── G6: Waitlist conversion rate ────────────────────────────────

    def test_waitlist_conversion_rate_real(self):
        aid = _create_amenity(max_capacity_per_slot=1, waitlist_mode='auto_confirm')
        r1 = self._book(aid, 673, 10)
        self.uc.cancel(r1.data['id'], reason='test')
        # Fill slot (1/1)
        r2 = self._book(aid, 674, 10)
        # Trigger waitlist via capacity exceeded (1 existing + 1 new > 1)
        r3 = self.uc.create(condominium_id=1, building_id=1, amenity_id=aid,
            unit_id=673, owner_id=12, booking_date=self.d,
            start_at=datetime(self.d.year,self.d.month,self.d.day,10,0),
            end_at=datetime(self.d.year,self.d.month,self.d.day,11,0), guest_count=1)
        assert r3.data.get('waitlist_entry_id'), f'Expected waitlist, got {r3.data}'
        # Free slot
        self.uc.cancel(r2.data['id'], reason='test')
        # Promote
        res = self.wl_uc.promote(aid, self.d, waitlist_mode='auto_confirm', condominium_id=1)
        assert res['booking_id'] is not None
        cr = self.ruc.waitlist_conversion_rate(aid, from_date=self.d-timedelta(1), to_date=self.d+timedelta(1))
        assert cr['total_waitlisted'] >= 1 and cr['total_converted'] >= 1

    # ── G7: Amenity distribution ────────────────────────────────────

    def test_amenity_distribution_with_data(self):
        aid = _create_amenity(max_capacity_per_slot=5)
        self._book(aid, 673, 10, guest_count=4)
        self._confirm_bookings(aid)
        dist = self.ruc.amenity_distribution(1, from_date=self.d-timedelta(1), to_date=self.d+timedelta(1))
        our = [d for d in dist if d['amenity_id'] == aid]
        assert len(our) >= 1, f"Missing amenity {aid} in distribution"
        assert our[0]['total_bookings'] >= 1 and our[0]['total_guests'] >= 4
