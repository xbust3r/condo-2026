"""
End-to-end tests: login → select-condo → dashboard flow.

Validates:
- POST /auth/login returns JWT + user
- GET /me/contexts returns roles_by_condominium + ownerships
- GET /residents/dashboard returns payment status + announcements
- GET /ar/user-summary returns debt summary
"""
import pytest
from datetime import date, datetime, timedelta
from decimal import Decimal
import uuid as _uuid


# ── Sandbox factories ───────────────────────────────────────────────────

from tests.factories.condo_factory import CondoFactory
from tests.factories.building_factory import BuildingFactory
from tests.factories.unit_factory import UnitFactory
from tests.factories.user_factory import UserFactory
from tests.factories.resident_factory import ResidentFactory


def _setup_e2e_sandbox(db_session):
    """Create user + condo + building + unit + ownership + role + resident profile."""
    tag = _uuid.uuid4().hex[:8]

    # 1. Condominium
    condo = CondoFactory.create(
        db_session, name=f"E2E Condo {tag}",
        code=f"E2E-{tag}",
        city="Lima", country="Perú",
    )

    # 2. Building
    building = BuildingFactory.create(
        db_session, condominium_id=condo.id,
        code=f"BLD-{tag}", name="Torre E2E",
        floors_count=5, units_planned=1,
    )

    # 3. Unit
    unit = UnitFactory.create(
        db_session, building_id=building.id,
        unit_number="101", code=f"U-{tag}",
        name="Unidad 101", floor_number=1,
        occupancy_status="occupied",
    )

    # 4. User (SHA256 + then bcrypt override for real auth)
    from library.dddpy.shared.utils.password import password as pwd_util
    bcrypt_hash = pwd_util.generate("E2ETestPass123!")
    user = UserFactory.create(
        db_session,
        email=f"e2e-{tag}@test.local",
        password="E2ETestPass123!",
    )
    from sqlalchemy import text
    db_session.execute(
        text("UPDATE users SET password_hash = :hash WHERE id = :uid"),
        {"hash": bcrypt_hash, "uid": user.id},
    )
    db_session.commit()

    # 5. Resident profile
    ResidentFactory.create(db_session, user_id=user.id, condominium_id=condo.id)

    # 6. User profile
    from library.dddpy.core_user_profiles.infrastructure.dbuser_profile import DBUserProfile
    from sqlalchemy import func as sa_func
    profile = DBUserProfile(
        uuid=str(_uuid.uuid4()),
        user_id=user.id,
        first_name="E2EUser",
        last_name=f"Test-{tag}",
        updated_at=sa_func.now(),
    )
    db_session.add(profile)
    db_session.flush()

    # 7. Unit ownership (links user → unit)
    from library.dddpy.core_unit_ownerships.infrastructure.dbunit_ownership import DBUnitOwnership
    ownership = DBUnitOwnership(
        uuid=str(_uuid.uuid4()),
        unit_id=unit.id,
        user_id=user.id,
        ownership_type="owner",
        ownership_percentage=Decimal("100.00"),
        status="active",
    )
    db_session.add(ownership)
    db_session.flush()

    # 8. Condominium role (so /me/contexts returns roles_by_condominium)
    from library.dddpy.core_condominium_roles.infrastructure.dbcondominium_role import DBCondominiumRoles
    role = DBCondominiumRoles(
        uuid=str(_uuid.uuid4()),
        condominium_id=condo.id,
        user_id=user.id,
        role="resident",
        status="active",
        scope="condominium",
    )
    db_session.add(role)
    db_session.flush()

    # 9. Announcement
    from library.dddpy.core_announcements.infrastructure.dbannouncement import DBAnnouncement
    announcement = DBAnnouncement(
        uuid=str(_uuid.uuid4()),
        condominium_id=condo.id,
        author_user_id=user.id,
        title="Bienvenido al condominio",
        content="Este es un comunicado de prueba para residentes.",
        category="info",
        visibility="public",
        published_at=datetime.utcnow(),
    )
    db_session.add(announcement)
    db_session.flush()

    db_session.commit()

    return {
        "tag": tag,
        "condo": condo,
        "building": building,
        "unit": unit,
        "user": user,
        "password": "E2ETestPass123!",
    }


# ── Cleanup ─────────────────────────────────────────────────────────────

_CASCADE_TABLES = [
    "core_amenity_bookings", "core_amenities",
    "core_announcements", "core_documents",
    "core_incidents", "core_meetings", "core_notifications",
    "core_packages", "core_visitors",
    "core_payments", "core_receipts",
    "core_ledger_entries",
    "core_accounts_receivable",
    "core_charges", "core_charge_types",
    "core_resident_profiles",
    "core_condominium_roles",
    "core_votes", "core_vote_options",
    "core_unit_ownerships", "core_unit_occupancies",
    "core_units",
    "core_buildings",
    "core_condominiums",
    "user_profiles",
]


def _cleanup_by_condo(db_session, condo_id: int):
    from sqlalchemy import text
    for table in _CASCADE_TABLES:
        try:
            db_session.execute(
                text(f"DELETE FROM {table} WHERE condominium_id = :cid"),
                {"cid": condo_id},
            )
        except Exception:
            pass
    db_session.commit()


# ── API helpers ─────────────────────────────────────────────────────────

def _login(email: str, password: str) -> dict:
    from library.dddpy.auth.usecase.auth_usecase import AuthUseCase
    uc = AuthUseCase()
    result = uc.login(email=email, password=password)
    return result.dict()


def _get_context(user_id: int) -> dict:
    """GET /me/contexts — full user context with roles, ownerships, etc."""
    from api.contexts.context_usecase import ContextUseCase
    uc = ContextUseCase()
    result = uc.get_user_context(user_id)
    return result


def _get_dashboard(condominium_id: int, user_id: int) -> dict:
    from library.dddpy.core_residents.usecase.resident_usecase import ResidentUseCase
    uc = ResidentUseCase()
    result = uc.get_dashboard(user_id=user_id, condominium_id=condominium_id)
    return result.dict()


def _get_ar_user_summary(condominium_id: int, user_id: int) -> dict:
    from library.dddpy.core_accounts_receivable.usecase.ar_usecase import ARUseCase
    uc = ARUseCase()
    result = uc.get_summary_by_user(condominium_id=condominium_id, user_id=user_id)
    return result.dict()


# ── Tests ───────────────────────────────────────────────────────────────

class TestLoginFlow:
    """POST /auth/login — authentication step."""

    def test_login_success(self, db_session):
        s = _setup_e2e_sandbox(db_session)

        result = _login(f"e2e-{s['tag']}@test.local", s["password"])
        data = result["data"]

        assert result["success"] is True
        assert "access_token" in data
        assert "refresh_token" in data
        assert len(data["access_token"]) > 20
        assert data["user"]["email"] == f"e2e-{s['tag']}@test.local"

        _cleanup_by_condo(db_session, s["condo"].id)

    def test_login_wrong_password(self, db_session):
        s = _setup_e2e_sandbox(db_session)

        with pytest.raises(Exception):
            _login(f"e2e-{s['tag']}@test.local", "WrongPassword!")

        _cleanup_by_condo(db_session, s["condo"].id)


class TestContextEndpoint:
    """GET /me/contexts — full user context with condominiums."""

    def test_context_returns_roles_and_ownerships(self, db_session):
        s = _setup_e2e_sandbox(db_session)

        ctx = _get_context(s["user"].id)

        assert ctx["user"]["email"] == f"e2e-{s['tag']}@test.local"
        assert "roles_by_condominium" in ctx
        assert len(ctx["roles_by_condominium"]) >= 1
        assert len(ctx["ownerships"]) >= 1

        _cleanup_by_condo(db_session, s["condo"].id)


class TestDashboardFlow:
    """GET /residents/dashboard — consolidated resident dashboard."""

    def test_dashboard_returns_payment_status(self, db_session):
        s = _setup_e2e_sandbox(db_session)

        dash = _get_dashboard(s["condo"].id, s["user"].id)
        data = dash["data"]

        assert dash["success"] is True
        assert "payment_pending_total" in data
        assert data["payment_pending_total"] == 0

        _cleanup_by_condo(db_session, s["condo"].id)

    def test_dashboard_with_debt(self, db_session):
        s = _setup_e2e_sandbox(db_session)

        from library.dddpy.core_accounts_receivable.infrastructure.dbar import DBAR
        ar = DBAR(
            uuid=str(_uuid.uuid4()),
            condominium_id=s["condo"].id,
            unit_id=s["unit"].id,
            debtor_user_id=s["user"].id,
            reference_code="MANT-2026-05",
            description="Cuota de mantenimiento Mayo 2026",
            amount=Decimal("350.00"),
            paid_amount=Decimal("0.00"),
            currency="PEN",
            status="pending",
            due_date=date.today() + timedelta(days=15),
            origin_type="charge",
        )
        db_session.add(ar)
        db_session.commit()

        dash = _get_dashboard(s["condo"].id, s["user"].id)
        data = dash["data"]
        assert data["payment_pending_total"] > 0

        _cleanup_by_condo(db_session, s["condo"].id)

    def test_dashboard_has_announcements(self, db_session):
        s = _setup_e2e_sandbox(db_session)

        dash = _get_dashboard(s["condo"].id, s["user"].id)
        data = dash["data"]

        assert "recent_announcements" in data
        announcements = data["recent_announcements"]
        assert len(announcements) >= 1
        assert announcements[0]["title"] == "Bienvenido al condominio"

        _cleanup_by_condo(db_session, s["condo"].id)


class TestSelectCondoFlow:
    """select-condo screen: user sees their assigned condominiums."""

    def test_user_sees_assigned_condo(self, db_session):
        s = _setup_e2e_sandbox(db_session)

        ctx = _get_context(s["user"].id)

        roles = ctx.get("roles_by_condominium", {})
        assert len(roles) > 0, "User must have condominium roles"

        # roles_by_condominium is a dict keyed by condo_id
        condo_ids = [int(k) for k in roles.keys()]
        assert s["condo"].id in condo_ids

        _cleanup_by_condo(db_session, s["condo"].id)


class TestARUserSummary:
    """GET /ar/user-summary — debt summary endpoint."""

    def test_user_summary_no_debt(self, db_session):
        s = _setup_e2e_sandbox(db_session)

        summary = _get_ar_user_summary(s["condo"].id, s["user"].id)
        data = summary["data"]

        assert summary["success"] is True
        assert data["is_up_to_date"] is True
        assert data["pending_amount"] == 0
        assert data["pending_count"] == 0
        assert data["currency"] == "PEN"

        _cleanup_by_condo(db_session, s["condo"].id)

    def test_user_summary_with_debt(self, db_session):
        s = _setup_e2e_sandbox(db_session)

        from library.dddpy.core_accounts_receivable.infrastructure.dbar import DBAR
        for month, amount in [("2026-04", Decimal("350.00")), ("2026-05", Decimal("350.00"))]:
            ar = DBAR(
                uuid=str(_uuid.uuid4()),
                condominium_id=s["condo"].id,
                unit_id=s["unit"].id,
                debtor_user_id=s["user"].id,
                reference_code=f"MANT-{month}",
                description=f"Cuota {month}",
                amount=amount,
                paid_amount=Decimal("0.00"),
                currency="PEN",
                status="pending",
                due_date=date.today() + timedelta(days=30),
                period=month,
                origin_type="charge",
            )
            db_session.add(ar)
        db_session.commit()

        summary = _get_ar_user_summary(s["condo"].id, s["user"].id)
        data = summary["data"]

        assert data["is_up_to_date"] is False
        assert data["pending_amount"] == 700.0
        assert data["pending_count"] == 2

        _cleanup_by_condo(db_session, s["condo"].id)

    def test_user_summary_excludes_paid(self, db_session):
        s = _setup_e2e_sandbox(db_session)

        from library.dddpy.core_accounts_receivable.infrastructure.dbar import DBAR
        paid = DBAR(
            uuid=str(_uuid.uuid4()),
            condominium_id=s["condo"].id,
            unit_id=s["unit"].id,
            debtor_user_id=s["user"].id,
            reference_code="MANT-PAID",
            description="Already paid",
            amount=Decimal("350.00"),
            paid_amount=Decimal("350.00"),
            currency="PEN",
            status="paid",
            due_date=date.today() - timedelta(days=30),
            origin_type="charge",
        )
        db_session.add(paid)
        db_session.commit()

        summary = _get_ar_user_summary(s["condo"].id, s["user"].id)
        data = summary["data"]

        assert data["is_up_to_date"] is True
        assert data["pending_amount"] == 0

        _cleanup_by_condo(db_session, s["condo"].id)


class TestFullE2EFlow:
    """Complete flow: login → /me/contexts → dashboard → ar/summary."""

    def test_complete_resident_flow(self, db_session):
        s = _setup_e2e_sandbox(db_session)

        # Step 1: Login
        login = _login(f"e2e-{s['tag']}@test.local", s["password"])
        assert login["success"], f"Login failed: {login.get('message')}"
        user_id = login["data"]["user"]["id"]

        # Step 2: Get contexts (select-condo data)
        ctx = _get_context(user_id)
        assert ctx["user"]["email"] == f"e2e-{s['tag']}@test.local"
        roles = ctx.get("roles_by_condominium", {})
        assert len(roles) > 0, "Must have at least one condominium role"

        # Step 3: Select condo (verify condo_id is in roles)
        condo_ids = [int(k) for k in roles.keys()]
        assert s["condo"].id in condo_ids

        # Step 4: Dashboard
        dash = _get_dashboard(s["condo"].id, user_id)
        assert dash["success"]
        dash_data = dash["data"]

        for key in ["payment_pending_total", "recent_announcements", "unread_notifications"]:
            assert key in dash_data, f"Dashboard missing key: {key}"

        # Step 5: AR summary
        ar_summary = _get_ar_user_summary(s["condo"].id, user_id)
        assert ar_summary["success"]
        assert ar_summary["data"]["is_up_to_date"] is True

        _cleanup_by_condo(db_session, s["condo"].id)
