"""Integration tests for core_votes — real MySQL/MariaDB.

Uses db_condo_testings with alembic migrations applied.
Tests full create → publish → cast_vote → proclaim flow with real SQL.

Run with:  PYTHONPATH=src pytest tests/test_core_votes_integration.py -v
"""
import sys
import os
from datetime import datetime, timedelta, timezone
from contextlib import contextmanager
from unittest.mock import patch
import uuid as uuid_lib
from itertools import count

import pytest
from sqlalchemy import text

# Shared frozen time for publish+cast+proclaim tests
FROZEN_NOW = datetime(2026, 6, 1, 12, 0, 0, 0)


class _FrozenDatetime(datetime):
    """datetime subclass whose utcnow()/now() always return FROZEN_NOW.

    Patch onto vote_cmd_usecase.datetime so publish / cast_vote / proclaim
    all see the same frozen moment."""
    @classmethod
    def utcnow(cls):
        return FROZEN_NOW

    @classmethod
    def now(cls, tz=None):
        return FROZEN_NOW.replace(tzinfo=tz) if tz else FROZEN_NOW


def _patch_datetime_on(module):
    """Convenience context-manager builder."""
    return patch.object(module, 'datetime', _FrozenDatetime)

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from tests.conftest import TestSessionLocal

# ── Globals ─────────────────────────────────────────────────────────────────

_counter = count(1)
# Not used directly in tests that need publish+cast — those use FROZEN_NOW + patch
_now = datetime.now(timezone.utc).replace(tzinfo=None)


def _snapshot_at():
    """ISO timestamp matching to_rules_snapshot_dict format."""
    return datetime.now(timezone.utc).isoformat()


def _uid():
    return str(uuid_lib.uuid4())


def _unique_unit_number():
    return f"{next(_counter):04d}"


@contextmanager
def db():
    s = TestSessionLocal()
    try:
        yield s
        s.commit()
    except Exception:
        s.rollback()
        raise
    finally:
        s.close()


# ═══════════════════════════════════════════════════════════════════════════════
#  Monkeypatch SessionLocal → TestSessionLocal
# ═══════════════════════════════════════════════════════════════════════════════

def _install_test_session():
    import library.dddpy.shared.mysql.base as base_mod
    base_mod._original_SessionLocal = base_mod.SessionLocal
    base_mod.SessionLocal = TestSessionLocal


def _restore_test_session():
    import library.dddpy.shared.mysql.base as base_mod
    if hasattr(base_mod, '_original_SessionLocal'):
        base_mod.SessionLocal = base_mod._original_SessionLocal
        del base_mod._original_SessionLocal


@pytest.fixture(autouse=True)
def _test_db_session_monkey():
    _install_test_session()
    yield
    _restore_test_session()


# ═══════════════════════════════════════════════════════════════════════════════
#  Seed helpers
# ═══════════════════════════════════════════════════════════════════════════════

def seed_condominium(session):
    uid = _uid()
    session.execute(
        text("""INSERT INTO core_condominiums (uuid, code, name, legal_name, status)
               VALUES (:uuid, :code, :name, :legal_name, :status)"""),
        {"uuid": uid, "code": f"CONDO-{uid[:8]}", "name": "Test Condominium",
         "legal_name": "Test Condo S.A.C.", "status": 1},
    )
    session.flush()
    return session.execute(text("SELECT id FROM core_condominiums WHERE uuid = :uid"), {"uid": uid}).scalar()


def seed_building(session, condominium_id):
    uid = _uid()
    session.execute(
        text("""INSERT INTO core_buildings (uuid, condominium_id, code, name, building_type_id, status)
               VALUES (:uuid, :condo, :code, :name, 1, 1)"""),
        {"uuid": uid, "condo": condominium_id, "code": f"BLD-{uid[:4]}", "name": "Torre A"},
    )
    session.flush()
    return session.execute(text("SELECT id FROM core_buildings WHERE uuid = :uid"), {"uid": uid}).scalar()


def seed_unit(session, building_id):
    uid = _uid()
    un = _unique_unit_number()
    session.execute(
        text("""INSERT INTO core_units (uuid, building_id, unit_number, code, name,
               private_area, coefficient, status)
               VALUES (:uuid, :bldg, :num, :code, :name, 75.0, 5.5, 1)"""),
        {"uuid": uid, "bldg": building_id, "num": un, "code": f"U-{un}", "name": f"Apto {un}"},
    )
    session.flush()
    return session.execute(text("SELECT id FROM core_units WHERE uuid = :uid"), {"uid": uid}).scalar()


def seed_user(session):
    uid = _uid()
    session.execute(
        text("""INSERT INTO users (uuid, email, password_hash, token_version, status)
               VALUES (:uuid, :email, :hash, 0, 1)"""),
        {"uuid": uid, "email": f"test-{uid[:8]}@test.com", "hash": "$2b$testhash"},
    )
    session.flush()
    user_id = session.execute(text("SELECT id FROM users WHERE uuid = :uid"), {"uid": uid}).scalar()

    session.execute(
        text("""INSERT INTO user_profiles (uuid, user_id, first_name, last_name)
               VALUES (:uuid, :uid, :fn, :ln)"""),
        {"uuid": _uid(), "uid": user_id, "fn": f"Test-{uid[:6]}", "ln": "User"},
    )
    session.flush()
    return user_id


def seed_unit_ownership(session, unit_id, user_id):
    uid = _uid()
    session.execute(
        text("""INSERT INTO core_unit_ownerships (uuid, unit_id, user_id, ownership_type, status)
               VALUES (:uuid, :unit, :user, 'owner', 'active')"""),
        {"uuid": uid, "unit": unit_id, "user": user_id},
    )
    session.flush()
    return session.execute(text("SELECT id FROM core_unit_ownerships WHERE uuid = :uid"), {"uid": uid}).scalar()


def seed_voting_rule(session, condominium_id, created_by_user_id, building_id=None, **overrides):
    uid = _uid()
    params = {
        "name": "Default rule", "owners_only": True, "max_debt_months": 2,
        "vote_calculation_type": "by_unit",
        "scope_type": "condominium" if building_id is None else "building",
        "is_active": True,
    }
    params.update(overrides)
    session.execute(
        text("""INSERT INTO core_voting_rules
               (uuid, condominium_id, building_id, name, owners_only, max_debt_months,
                allow_tenants, vote_calculation_type, include_parking, include_annexes,
                scope_type, is_active, created_by_user_id)
               VALUES (:uuid, :condo, :bldg, :name, :owners_only, :max_debt_months,
                FALSE, :vote_calculation_type, FALSE, FALSE,
                :scope_type, :is_active, :created_by_user_id)"""),
        {"uuid": uid, "condo": condominium_id, "bldg": building_id,
         "name": params["name"], "owners_only": params["owners_only"],
         "max_debt_months": params["max_debt_months"],
         "vote_calculation_type": params["vote_calculation_type"],
         "scope_type": params["scope_type"],
         "is_active": params["is_active"],
         "created_by_user_id": created_by_user_id},
    )
    session.flush()
    return session.execute(text("SELECT id FROM core_voting_rules WHERE uuid = :uid"), {"uid": uid}).scalar()


# ═══════════════════════════════════════════════════════════════════════════════
#  Reusable permissive snapshot dict
# ═══════════════════════════════════════════════════════════════════════════════

def make_snapshot(**overrides):
    """Build a rules_snapshot dict matching VotingRulesSnapshot.from_dict() contract."""
    d = {
        "snapshot_at": _snapshot_at(),
        "snapshot_version": 1,
        "vote_calculation_type": "by_unit",
        "scope": "condominium",
        "building_id": None,
        "allow_only_owners": True,
        "allow_tenants": False,
        "max_debt_months": "0",
        "include_parking_storage": False,
    }
    d.update(overrides)
    return d


# ═══════════════════════════════════════════════════════════════════════════════
#  Integration tests
# ═══════════════════════════════════════════════════════════════════════════════

class TestVoteIntegration:

    def test_tables_exist_with_all_columns(self):
        """All vote tables + columns exist after alembic migrations."""
        with db() as s:
            tables = ["core_votes", "core_vote_options", "core_vote_records",
                      "voter_eligibility_log", "voter_eligibility_reason_codes",
                      "core_voting_rules"]
            for t in tables:
                s.execute(text(f"SELECT 1 FROM {t} LIMIT 0"))

            cols = {c[0] for c in s.execute(text("SHOW COLUMNS FROM core_votes")).fetchall()}
            for c in ["scope_type", "vote_calculation_type", "building_id", "rules_snapshot"]:
                assert c in cols, f"Missing column: {c}"

            rec_cols = {c[0] for c in s.execute(text("SHOW COLUMNS FROM core_vote_records")).fetchall()}
            assert "unit_ownership_id" in rec_cols
            assert "weight" in rec_cols

    def test_full_create_vote_and_cast_flow(self):
        """End-to-end: create → publish → cast → verify DB state.

        Patches the usecase module's datetime ref so utcnow() returns
        a frozen timestamp, allowing both publish (voting_starts_at >= now)
        and cast_vote (start <= now <= end) to pass reliably."""
        from library.dddpy.core_votes.usecase.vote_factory import vote_cmd_usecase_factory
        from library.dddpy.core_votes.usecase import vote_cmd_usecase as uc_mod
        from library.dddpy.core_votes.usecase.vote_cmd_schema import CreateVoteSchema

        with db() as s:
            condo_id = seed_condominium(s)
            building_id = seed_building(s, condo_id)
            unit_id = seed_unit(s, building_id)
            user_id = seed_user(s)
            uo_id = seed_unit_ownership(s, unit_id, user_id)

        cmd_uc = vote_cmd_usecase_factory()
        req = CreateVoteSchema(
            condominium_id=condo_id, title="Integration Test Vote",
            voting_starts_at=FROZEN_NOW,
            voting_ends_at=FROZEN_NOW + timedelta(days=7),
            options=[
                {"option_text": "Sí", "option_key": "yes"},
                {"option_text": "No", "option_key": "no"},
            ],
            rules_snapshot=make_snapshot(),
        )
        entity = cmd_uc.create(data=req, created_by_user_id=user_id)
        vote_id = entity.id
        assert vote_id > 0

        with _patch_datetime_on(uc_mod):
            entity = cmd_uc.publish(id=vote_id)
            assert entity.status == "active"

            assert cmd_uc.cast_vote(vote_id=vote_id, user_id=user_id,
                                    unit_ownership_id=uo_id, option_key="yes") is True

        with db() as s:
            v = s.execute(text("SELECT * FROM core_votes WHERE id = :id"), {"id": vote_id}).mappings().fetchone()
            assert v["title"] == "Integration Test Vote"
            assert v["total_votes_cast"] == 1
            assert v["total_yes_votes"] == 1

            rec = s.execute(text("SELECT * FROM core_vote_records WHERE vote_id = :vid"), {"vid": vote_id}).mappings().fetchone()
            assert rec is not None
            assert rec["option_key"] == "yes"
            assert rec["unit_ownership_id"] == uo_id
            assert float(rec["weight"]) == 1.0

            log = s.execute(text("SELECT * FROM voter_eligibility_log WHERE vote_id = :vid"), {"vid": vote_id}).mappings().fetchone()
            assert log is not None

    def test_duplicate_vote_rejected(self):
        """UNIQUE (vote_id, unit_ownership_id) rejects second vote from same unit."""
        from library.dddpy.core_votes.usecase.vote_factory import vote_cmd_usecase_factory
        from library.dddpy.core_votes.usecase.vote_cmd_schema import CreateVoteSchema
        from library.dddpy.core_votes.domain.vote_exception import AlreadyVoted

        with db() as s:
            condo_id = seed_condominium(s)
            unit_id = seed_unit(s, seed_building(s, condo_id))
            user_id = seed_user(s)
            uo_id = seed_unit_ownership(s, unit_id, user_id)

        cmd_uc = vote_cmd_usecase_factory()
        req = CreateVoteSchema(
            condominium_id=condo_id, title="Test Duplicate",
            voting_starts_at=FROZEN_NOW,
            voting_ends_at=FROZEN_NOW + timedelta(days=7),
            options=[
                {"option_text": "Sí", "option_key": "yes"},
                {"option_text": "No", "option_key": "no"},
            ],
            rules_snapshot=make_snapshot(),
        )
        entity = cmd_uc.create(data=req, created_by_user_id=user_id)

        from library.dddpy.core_votes.usecase import vote_cmd_usecase as uc_mod
        with _patch_datetime_on(uc_mod):
            cmd_uc.publish(id=entity.id)
            assert cmd_uc.cast_vote(entity.id, user_id, uo_id, "yes") is True

            with pytest.raises(AlreadyVoted):
                cmd_uc.cast_vote(entity.id, user_id, uo_id, "yes")

    def test_arrears_reader_real_sql(self):
        """ArrearsSqlReader queries core_accounts_receivable correctly."""
        from library.dddpy.core_arrears.infrastructure.arrears_sql_reader import ArrearsSqlReader

        with db() as s:
            condo_id = seed_condominium(s)
            bldg = seed_building(s, condo_id)
            unit_a = seed_unit(s, bldg)
            unit_b = seed_unit(s, bldg)

            now = _now
            s.execute(
                text("""INSERT INTO core_accounts_receivable
                       (uuid, condominium_id, unit_id, charge_id, debtor_user_id, description,
                        amount, paid_amount, due_date, period, status, created_at)
                       VALUES
                       (:u1, :condo, :ua, NULL, 1, 'Mto Ene', 100, 0, :past, '2026-01', 'pending', :now),
                       (:u2, :condo, :ua, NULL, 1, 'Mto Feb', 100, 0, :future, '2026-05', 'pending', :now),
                       (:u3, :condo, :ub, NULL, 1, 'Mto Ene', 100, 100, :past, '2026-01', 'paid', :now)"""),
                {"u1": _uid(), "u2": _uid(), "u3": _uid(),
                 "condo": condo_id, "ua": unit_a, "ub": unit_b,
                 "past": now - timedelta(days=60), "future": now + timedelta(days=30), "now": now},
            )
            s.commit()

        reader = ArrearsSqlReader()
        a = reader.get_arrears(unit_a)
        assert a.months_in_arrears >= 1, f"Expected >=1, got {a.months_in_arrears}"
        assert a.total_overdue > 0

        b = reader.get_arrears(unit_b)
        assert b.months_in_arrears == 0
        assert b.total_overdue == 0

        x = reader.get_arrears(999999)
        assert x.months_in_arrears == 0
        assert x.oldest_period is None

    def test_voting_rule_repo_real_sql(self):
        """VotingRuleQueryRepository queries core_voting_rules correctly."""
        from library.dddpy.core_votes.infrastructure.voting_rule_query_repository import (
            VotingRuleQueryRepository,
        )

        with db() as s:
            condo_id = seed_condominium(s)
            bldg = seed_building(s, condo_id)
            user_id = seed_user(s)
            seed_voting_rule(s, condo_id, user_id, name="Condo Rule",
                             scope_type="condominium", vote_calculation_type="by_unit")
            seed_voting_rule(s, condo_id, user_id, building_id=bldg, name="Building Rule",
                             scope_type="building", vote_calculation_type="by_coefficient")
            seed_voting_rule(s, condo_id, user_id, name="Inactive", is_active=False)
            s.commit()

        repo = VotingRuleQueryRepository()
        rules = repo.find_active(condo_id)
        assert rules is not None, "Should find at least the condominium-wide rule"

        snapshots = [VotingRuleQueryRepository.to_rules_snapshot_dict(rules)]
        assert len(snapshots) == 1
        assert "vote_calculation_type" in snapshots[0]

    def test_handles_empty_tables(self):
        """Readers return sensible defaults on empty tables."""
        from library.dddpy.core_arrears.infrastructure.arrears_sql_reader import ArrearsSqlReader
        from library.dddpy.core_votes.infrastructure.voting_rule_query_repository import (
            VotingRuleQueryRepository,
        )

        reader = ArrearsSqlReader()
        r = reader.get_arrears(999999)
        assert r.months_in_arrears == 0
        assert r.oldest_period is None

        repo = VotingRuleQueryRepository()
        rules = repo.find_active(999999)
        assert rules is None

    def test_counters_accurate_after_multiple_casts(self):
        """Vote counters reflect all cast votes."""
        from library.dddpy.core_votes.usecase.vote_factory import vote_cmd_usecase_factory
        from library.dddpy.core_votes.usecase.vote_cmd_schema import CreateVoteSchema

        with db() as s:
            condo_id = seed_condominium(s)
            bldg = seed_building(s, condo_id)
            ua = seed_unit(s, bldg)
            ub = seed_unit(s, bldg)
            uc = seed_unit(s, bldg)
            u1 = seed_user(s)
            u2 = seed_user(s)
            u3 = seed_user(s)
            oa = seed_unit_ownership(s, ua, u1)
            ob = seed_unit_ownership(s, ub, u2)
            oc = seed_unit_ownership(s, uc, u3)

        cmd_uc = vote_cmd_usecase_factory()
        req = CreateVoteSchema(
            condominium_id=condo_id, title="Multi Vote",
            voting_starts_at=FROZEN_NOW,
            voting_ends_at=FROZEN_NOW + timedelta(days=7),
            options=[
                {"option_text": "Sí", "option_key": "yes"},
                {"option_text": "No", "option_key": "no"},
                {"option_text": "Abstención", "option_key": "abstain"},
            ],
            rules_snapshot=make_snapshot(),
        )
        entity = cmd_uc.create(data=req, created_by_user_id=u1)
        vid = entity.id

        from library.dddpy.core_votes.usecase import vote_cmd_usecase as uc_mod
        with _patch_datetime_on(uc_mod):
            cmd_uc.publish(id=vid)
            cmd_uc.cast_vote(vid, u1, oa, "yes")
            cmd_uc.cast_vote(vid, u2, ob, "no")
            cmd_uc.cast_vote(vid, u3, oc, "abstain")

        with db() as s:
            v = s.execute(
                text("""SELECT total_votes_cast, total_yes_votes, total_no_votes, total_abstain_votes
                       FROM core_votes WHERE id = :id"""), {"id": vid}
            ).mappings().fetchone()
            assert v["total_votes_cast"] == 3
            assert v["total_yes_votes"] == 1
            assert v["total_no_votes"] == 1
            assert v["total_abstain_votes"] == 1

    def test_proclaim_result_approved(self):
        """create → publish → cast → proclaim: full lifecycle."""
        from library.dddpy.core_votes.usecase.vote_factory import vote_cmd_usecase_factory
        from library.dddpy.core_votes.usecase import vote_cmd_usecase as uc_mod
        from library.dddpy.core_votes.usecase.vote_cmd_schema import CreateVoteSchema

        with db() as s:
            condo_id = seed_condominium(s)
            building_id = seed_building(s, condo_id)
            ua = seed_unit(s, building_id)
            ub = seed_unit(s, building_id)
            u1 = seed_user(s)
            u2 = seed_user(s)
            u3 = seed_user(s)
            o1 = seed_unit_ownership(s, ua, u1)
            o2 = seed_unit_ownership(s, ub, u2)
            o3 = seed_unit_ownership(s, ub, u3)
            seed_voting_rule(s, condo_id, u1, building_id=None,
                             owners_only=True, max_debt_months=0)
            s.flush()

        cmd_uc = vote_cmd_usecase_factory()
        req = CreateVoteSchema(
            condominium_id=condo_id, title="Proclaim Test",
            voting_starts_at=FROZEN_NOW,
            voting_ends_at=FROZEN_NOW + timedelta(days=7),
            options=[
                {"option_text": "Sí", "option_key": "yes"},
                {"option_text": "No", "option_key": "no"},
            ],
            rules_snapshot=make_snapshot(),
        )
        entity = cmd_uc.create(data=req, created_by_user_id=u1)
        vid = entity.id

        with _patch_datetime_on(uc_mod):
            cmd_uc.publish(id=vid)
            cmd_uc.cast_vote(vid, u1, o1, "yes")
            cmd_uc.cast_vote(vid, u2, o2, "no")
            cmd_uc.cast_vote(vid, u3, o3, "yes")
            result = cmd_uc.proclaim(vote_id=vid)
            # 2 yes + 1 no → 2/3 >= 0.5 → APPROVED
            assert result.status == "approved"

        with db() as s:
            v = s.execute(
                text("SELECT status, result_proclaimed_at FROM core_votes WHERE id = :id"),
                {"id": vid},
            ).mappings().fetchone()
            assert v["status"] == "approved"
            assert v["result_proclaimed_at"] is not None

    def test_scoped_to_building(self):
        """Vote with scope_type='building' stores building_id."""
        from library.dddpy.core_votes.usecase.vote_factory import vote_cmd_usecase_factory
        from library.dddpy.core_votes.usecase.vote_cmd_schema import CreateVoteSchema

        with db() as s:
            condo_id = seed_condominium(s)
            building_id = seed_building(s, condo_id)

        cmd_uc = vote_cmd_usecase_factory()
        req = CreateVoteSchema(
            condominium_id=condo_id, title="Building Scoped",
            voting_starts_at=_now - timedelta(hours=1),
            voting_ends_at=_now + timedelta(days=7),
            options=[
                {"option_text": "Sí", "option_key": "yes"},
                {"option_text": "No", "option_key": "no"},
            ],
            rules_snapshot=make_snapshot(
                scope="building",
                building_id=building_id,
                vote_calculation_type="by_coefficient",
            ),
        )
        entity = cmd_uc.create(data=req, created_by_user_id=1)
        vid = entity.id

        with db() as s:
            v = s.execute(
                text("SELECT scope_type, vote_calculation_type, building_id FROM core_votes WHERE id = :id"),
                {"id": vid},
            ).mappings().fetchone()
            assert v["scope_type"] == "building"
            assert v["vote_calculation_type"] == "by_coefficient"
            assert v["building_id"] == building_id
