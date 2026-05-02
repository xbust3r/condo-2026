"""
Smoke test: verify the integration sandbox creates and cleans up correctly.
"""
import pytest
from tests.support.integration_sandbox import create_integration_sandbox, sandbox_cleanup


class TestIntegrationSandbox:
    """Verify the full sandbox lifecycle."""

    def test_create_and_cleanup_full_sandbox(self, db_session):
        """
        Full lifecycle: create sandbox -> verify entities -> cleanup -> verify empty.
        """
        sandbox = create_integration_sandbox(db_session, condo_name="Smoke Test Condo")
        db_session.flush()

        # Verify all expected entity counts
        assert sandbox["condo"].id is not None
        assert sandbox["condo"].name == "Smoke Test Condo"
        assert len(sandbox["buildings"]) == 2
        assert len(sandbox["units"]) == 6
        assert len(sandbox["users"]) == 6
        assert len(sandbox["residents"]) == 6
        assert len(sandbox["charge_types"]) == 3
        assert len(sandbox["charges"]) == 5
        assert len(sandbox["ar_entries"]) == 3
        assert len(sandbox["payments"]) == 2
        assert len(sandbox["receipts"]) == 2
        assert len(sandbox["ledger_entries"]) >= 1
        assert len(sandbox["incidents"]) >= 1
        assert len(sandbox["visitors"]) >= 1
        assert len(sandbox["documents"]) == 2
        assert len(sandbox["meetings"]) == 1
        assert len(sandbox["votes"]) == 1
        assert len(sandbox["announcements"]) == 2
        assert len(sandbox["notifications"]) >= 1
        assert len(sandbox["packages"]) >= 1
        assert len(sandbox["amenities"]) == 2

        # Verify relationships
        for charge in sandbox["charges"]:
            assert charge.condominium_id == sandbox["condo"].id

        for ar in sandbox["ar_entries"]:
            assert ar.condominium_id == sandbox["condo"].id

        for payment in sandbox["payments"]:
            assert payment.condominium_id == sandbox["condo"].id

        # Cleanup
        condo_id = sandbox["condo"].id
        sandbox_cleanup(db_session, sandbox)
        db_session.flush()

        from library.dddpy.core_condominiums.infrastructure.dbcondominiums import DBCondominiums
        condo_check = db_session.get(DBCondominiums, condo_id)
        assert condo_check is None

    def test_minimal_sandbox(self, db_session):
        """Smaller sandbox: 1 building, 1 unit, 1 user."""
        sandbox = create_integration_sandbox(
            db_session,
            condo_name="Minimal Sandbox",
            buildings_count=1,
            units_per_building=1,
        )
        db_session.flush()

        assert len(sandbox["buildings"]) == 1
        assert len(sandbox["units"]) == 1
        assert len(sandbox["users"]) == 1
        assert len(sandbox["residents"]) == 1
        assert len(sandbox["charges"]) >= 1
        assert len(sandbox["charge_types"]) == 3

        sandbox_cleanup(db_session, sandbox)
        db_session.flush()
