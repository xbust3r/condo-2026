"""
Pytest configuration — db_condo_testings Infrastructure.

Provides:
- Session-scoped setup/teardown for db_condo_testings
- Database session fixture with auto-rollback per test
- Test data registry for tracking created records
- Factory + scenario builder support

Strategy: Option C (create per run → destroy per run)
"""
import os
import sys
import pytest
from decimal import Decimal
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

# ── Path setup ──────────────────────────────────────────────────────────────
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(PROJECT_ROOT, "src"))


# ── Load test environment ────────────────────────────────────────────────────
def _load_env():
    """Load .env.test into os.environ before anything else."""
    env_path = os.path.join(PROJECT_ROOT, ".env.test")
    if os.path.exists(env_path):
        with open(env_path) as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    key, _, value = line.partition("=")
                    os.environ.setdefault(key.strip(), value.strip())


_load_env()

# ── SQLAlchemy engine for tests ───────────────────────────────────────────────
DB_USER = os.environ.get("MYSQL_USER", "root")
DB_PASSWORD = os.environ.get("MYSQL_PASSWORD", "123456")
DB_HOST = os.environ.get("MYSQL_HOST", "mysql")
DB_PORT = os.environ.get("MYSQL_PORT", "3306")
DB_NAME = os.environ.get("MYSQL_DB", "db_condo_testings")

TEST_DATABASE_URL = (
    f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}?charset=utf8mb4"
)

test_engine = create_engine(TEST_DATABASE_URL, echo=False)
TestSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)


# ── DB lifecycle helpers ─────────────────────────────────────────────────────
def _create_test_database():
    """Create db_condo_testings from a clean slate (drops if exists)."""
    init_url = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/?charset=utf8mb4"
    init_engine = create_engine(init_url, echo=False)
    with init_engine.connect() as conn:
        # Kill active connections to this DB before dropping
        try:
            conn.execute(text(
                f"SELECT CONCAT('KILL ', id) FROM INFORMATION_SCHEMA.PROCESSLIST WHERE db = '{DB_NAME}'"
            ))
        except Exception:
            pass  # No connections to kill — fine
        conn.execute(text(f"DROP DATABASE IF EXISTS {DB_NAME}"))
        conn.execute(text(f"CREATE DATABASE {DB_NAME} CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci"))
        conn.commit()
    init_engine.dispose()
    # Pre-create alembic_version with VARCHAR(64) to avoid truncation
    db_engine = create_engine(TEST_DATABASE_URL, echo=False)
    with db_engine.connect() as conn:
        conn.execute(text(
            "CREATE TABLE IF NOT EXISTS alembic_version ("
            "  version_num VARCHAR(64) NOT NULL, "
            "  PRIMARY KEY (version_num)"
            ") ENGINE=InnoDB"
        ))
        conn.commit()
    db_engine.dispose()


def _run_alembic_migrations():
    """Run alembic migrations against db_condo_testings."""
    src_path = os.path.join(PROJECT_ROOT, "src")
    import subprocess

    env = os.environ.copy()
    env["MYSQL_DB"] = DB_NAME
    env["PYTHONPATH"] = src_path

    # Stamp the final common revision (052) which is the convergence point
    # of all 4 heads: 036 (amenities branch) and 049 (audit_logs branch) each
    # lead to 052. By stamping 052 as applied, alembic won't try to replay any
    # partial migration chain.
    result = subprocess.run(
        ["alembic", "stamp", "052_add_amenity_scope_and_building"],
        cwd=src_path,
        env=env,
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        # Fallback: try stamping the two branch heads separately
        for head in ["036_create_core_amenities", "049_create_core_audit_logs"]:
            r = subprocess.run(
                ["alembic", "stamp", head],
                cwd=src_path,
                env=env,
                capture_output=True,
                text=True,
            )
            if r.returncode != 0:
                print(f"[conftest] stamp {head} warning: {r.stderr[:200]}")

    result = subprocess.run(
        ["alembic", "upgrade", "052_add_amenity_scope_and_building"],
        cwd=src_path,
        env=env,
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        raise RuntimeError(
            f"Alembic migrations failed:\nSTDOUT:\n{result.stdout}\nSTDERR:\n{result.stderr}"
        )


def _drop_test_database():
    """Drop db_condo_testings completely."""
    init_url = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/?charset=utf8mb4"
    init_engine = create_engine(init_url, echo=False)
    try:
        with init_engine.connect() as conn:
            # Kill any active connections first
            conn.execute(
                text(
                    f"SELECT CONCAT('KILL ', id, ';') FROM INFORMATION_SCHEMA.PROCESSLIST WHERE db = '{DB_NAME}'"
                )
            )
            conn.execute(text(f"DROP DATABASE IF EXISTS {DB_NAME}"))
            conn.commit()
    finally:
        init_engine.dispose()


# ── Session fixtures ─────────────────────────────────────────────────────────

@pytest.fixture(scope="session", autouse=True)
def setup_test_db():
    """Create and migrate db_condo_testings once per test session."""
    _create_test_database()
    _run_alembic_migrations()
    yield
    # teardown handled by teardown_test_db


@pytest.fixture(scope="session", autouse=True)
def teardown_test_db():
    """Drop db_condo_testings at the end of the session."""
    yield
    _drop_test_database()


@pytest.fixture
def db_session():
    """
    Provide a SQLAlchemy session for a single test.
    Uses a transaction — auto-rollback on exit.
    """
    session = TestSessionLocal()
    try:
        yield session
    finally:
        session.rollback()
        session.close()


# ── Test data registry ───────────────────────────────────────────────────────

class TestDataRegistry:
    """
    Tracks records created during a test for debugging and cleanup.

    Usage:
        registry = TestDataRegistry()
        registry.register("core_condominiums", condo.id, condo.uuid)
        registry.register("core_buildings", bldg.id, bldg.uuid)
        yield registry
    """

    def __init__(self):
        self._data = {}  # {table_name: [{"id": ..., "uuid": ...}, ...]}

    def register(self, table: str, record_id: int, uuid: str = None):
        if table not in self._data:
            self._data[table] = []
        self._data[table].append({"id": record_id, "uuid": uuid})

    def get_ids(self, table: str) -> list[int]:
        return [r["id"] for r in self._data.get(table, [])]

    def all(self) -> dict:
        return dict(self._data)

    def clear(self):
        self._data.clear()


@pytest.fixture
def test_data_registry(db_session):
    """Fixture that provides a clean TestDataRegistry per test."""
    registry = TestDataRegistry()
    yield registry
    registry.clear()


# ── Sample entity fixtures (used across multiple test files) ──────────────────

@pytest.fixture
def sample_building_entity():
    """Sample BuildingEntity with all fields populated."""
    from library.dddpy.core_buildings.domain.building_entity import BuildingEntity
    from datetime import datetime
    from decimal import Decimal

    return BuildingEntity(
        id=1,
        uuid="test-uuid-1234",
        condominium_id=1,
        code="BLD-A",
        name="Torre A",
        short_name="Torre A",
        description="Building A description",
        building_type_id=1,
        built_area=Decimal("1500.0000"),
        common_area=Decimal("350.0000"),
        coefficient=Decimal("25.500000"),
        floors_count=10,
        basements_count=2,
        units_planned=20,
        sort_order=1,
        status=1,
        created_at=datetime(2026, 1, 1, 12, 0, 0),
        updated_at=datetime(2026, 1, 1, 12, 0, 0),
        deleted_at=None,
    )


@pytest.fixture
def sample_building_data():
    """Sample CreateBuildingData with all fields populated."""
    from library.dddpy.core_buildings.domain.building_data import CreateBuildingData
    from decimal import Decimal

    return CreateBuildingData(
        condominium_id=1,
        code="BLD-A",
        name="Torre A",
        short_name="Torre A",
        description="Building A description",
        building_type_id=1,
        built_area=Decimal("1500.0000"),
        common_area=Decimal("500.0000"),
        coefficient=Decimal("25.500000"),
        floors_count=10,
        basements_count=2,
        units_planned=20,
        sort_order=1,
    )
