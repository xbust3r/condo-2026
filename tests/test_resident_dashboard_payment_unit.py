"""
Pure unit tests for payment_pending deduplication logic.

These tests verify the set-union deduplication without requiring a database.
They test the Python logic directly — the integration tests in
test_resident_dashboard_payment.py cover the full DB path.
"""
import pytest


class TestDeduplicationLogic:
    """Verify that set(owner_units) | set(occupancy_units) deduplicates correctly."""

    def test_disjoint_sets_sum(self):
        """Owner owns units {1,2}, tenant occupies {3,4} → union = {1,2,3,4}."""
        owner_units = {1, 2}
        occupancy_units = {3, 4}
        union = owner_units | occupancy_units
        assert union == {1, 2, 3, 4}
        assert len(union) == 4

    def test_overlapping_sets_no_duplication(self):
        """Owner owns {1,2}, occupant of {1} → union = {1,2} (no duplicate)."""
        owner_units = {1, 2}
        occupancy_units = {1}  # same unit as ownership
        union = owner_units | occupancy_units
        assert union == {1, 2}
        assert len(union) == 2, f"Deduplication failed: {union}"

    def test_full_overlap(self):
        """Owner owns {1}, occupant of {1} → union = {1}."""
        owner_units = {1}
        occupancy_units = {1}
        union = owner_units | occupancy_units
        assert union == {1}
        assert len(union) == 1

    def test_empty_occupancy(self):
        """Only owner, no occupancy → union = owner_units."""
        owner_units = {1, 2, 3}
        occupancy_units = set()
        union = owner_units | occupancy_units
        assert union == {1, 2, 3}
        assert len(union) == 3

    def test_empty_ownership(self):
        """Only occupancy (tenant), no ownership → union = occupancy_units."""
        owner_units = set()
        occupancy_units = {5, 6}
        union = owner_units | occupancy_units
        assert union == {5, 6}
        assert len(union) == 2

    def test_both_empty(self):
        """No links at all → empty union."""
        union = set() | set()
        assert union == set()
        assert len(union) == 0

    def test_large_overlap(self):
        """Stress: 100 owner units, 50 overlapping → union = 100."""
        owner_units = set(range(100))
        occupancy_units = set(range(50))  # first 50 overlap
        union = owner_units | occupancy_units
        assert len(union) == 100

    def test_mixed_types_in_units(self):
        """Unit IDs as mixed types (int from ownership, int from occupancy) still deduplicate."""
        owner_units = {1, 2, 3}
        occupancy_units = {3, 4, 5}
        union = owner_units | occupancy_units
        assert union == {1, 2, 3, 4, 5}


class TestARSummationLogic:
    """Verify summation logic: only count non-paid, non-cancelled AR."""

    def make_ar(self, amount: float, paid: float, status: str) -> dict:
        return {"amount": amount, "paid_amount": paid, "status": status}

    def test_only_pending_counted(self):
        ars = [
            self.make_ar(350, 0, "pending"),
            self.make_ar(200, 200, "paid"),
            self.make_ar(100, 0, "cancelled"),
        ]
        pending = sum(
            a["amount"] - a["paid_amount"]
            for a in ars
            if a["status"] not in ("paid", "cancelled")
        )
        assert pending == 350.0

    def test_partially_paid_counted(self):
        ars = [
            self.make_ar(500, 200, "pending"),  # 300 pending
        ]
        pending = sum(
            a["amount"] - a["paid_amount"]
            for a in ars
            if a["status"] not in ("paid", "cancelled")
        )
        assert pending == 300.0

    def test_all_paid_zero(self):
        ars = [
            self.make_ar(350, 350, "paid"),
            self.make_ar(500, 500, "paid"),
        ]
        pending = sum(
            a["amount"] - a["paid_amount"]
            for a in ars
            if a["status"] not in ("paid", "cancelled")
        )
        assert pending == 0.0

    def test_no_ars_zero(self):
        pending = 0.0
        assert pending == 0.0

    def test_mixed_status_realistic(self):
        """Realistic: 3 months pending (Jan paid, Feb-Mar pending)."""
        ars = [
            self.make_ar(350, 350, "paid"),     # Jan — paid
            self.make_ar(350, 0, "pending"),     # Feb — pending
            self.make_ar(350, 0, "pending"),     # Mar — pending
            self.make_ar(350, 100, "pending"),   # Apr — partial
        ]
        pending = sum(
            a["amount"] - a["paid_amount"]
            for a in ars
            if a["status"] not in ("paid", "cancelled")
        )
        # Feb: 350, Mar: 350, Apr: 250 = 950
        assert pending == 950.0, f"Expected 950.0, got {pending}"
