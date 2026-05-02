# Testing Infrastructure — db_condo_testings

## Overview

This document describes the testing infrastructure for `condo-py`, using **`db_condo_testings`** as the isolated test database.

**Strategy: Option C**
- Create a dedicated test database per test run
- Run real migrations against it
- Execute the test suite
- Destroy/reset the database at the end of the run

---

## Database Configuration

### `.env.test`

A dedicated environment file for tests. **This file is gitignored.**

```env
MYSQL_USER=root
MYSQL_PASSWORD=123456
MYSQL_HOST=mysql
MYSQL_DB=db_condo_testings
MYSQL_PORT=3306

JWT_ACCESS_SECRET=<from src/.env>
JWT_REFRESH_SECRET=<from src/.env>
SECRET=<from src/.env>
BOOM_USER=<from src/.env>
BOOM_PASS=<from src/.env>
BOOM_SLUG=<from src/.env>
BUCKET=<from src/.env>
URL_SERVICE_BOOM=<from src/.env>
```

> **⚠️ Only for local development.** In CI, credentials are injected via secrets manager.

---

## Test Database Lifecycle

### Local Development

The test database is created and destroyed **per test run session** using pytest hooks in `conftest.py`:

```
db_condo_testings (empty)
    ↓ [pytest fixture: setup_test_db]
migrate all alembic migrations
    ↓
run tests (each test inserts its scenario)
    ↓ [pytest fixture: teardown_test_db]
drop all tables (or drop the whole DB)
```

### CI/CD Pipeline

```
1. CREATE DATABASE db_condo_testings;
2. alembic upgrade head
3. pytest tests/
4. DROP DATABASE db_condo_testings;
```

---

## Alembic Migrations on Test DB

Alembic is used for schema management. All migrations are applied against `db_condo_testings` before the suite runs.

To run migrations manually:

```bash
# Using the test env
cd src && alembic upgrade head

# Downgrade if needed
cd src && alembic downgrade -1
```

---

## Environment Variables in Tests

Pytest loads `.env.test` automatically via `python-dotenv` (if configured in `conftest.py`). All modules under `library/` read `MYSQL_DB=db_condo_testings`, ensuring complete isolation from `db_condominiums`.

### How it works

1. `conftest.py` sets `PYTHONPATH=src` and loads `.env.test`
2. All MySQL connection strings resolve to `db_condo_testings`
3. No test ever touches `db_condominiums` (production/development DB)

---

## Fixture Architecture

### Core Fixtures (`tests/conftest.py`)

| Fixture | Scope | Purpose |
|---|---|---|
| `setup_test_db` | session | Creates DB + runs migrations once before all tests |
| `teardown_test_db` | session | Destroys/resets DB after all tests complete |
| `db_session` | function | Provides a clean DB session per test |
| `test_data_registry` | function | Tracks IDs/UUIDs created in the current test |

### Factory Fixtures (`tests/factories/`)

Factories generate test data using the actual domain models:

- `condo_factory.py` — CondominiumEntity
- `building_factory.py` — BuildingEntity
- `unit_factory.py` — UnityEntity
- `user_factory.py` — UserEntity
- `resident_factory.py` — ResidentEntity

### Scenario Builder (`tests/support/scenario_builder.py`)

High-level scenarios that create complete data graphs:

- `create_full_condo_scenario()` — condo + buildings + units + users + residents
- `create_condo_with_1_building_3_units()` — minimal useful scenario
- `create_condo_with_residents()`

---

## Test Data Registry

Every test that creates data should register it in `test_data_registry`. This enables:

- **Debugging**: track what was created
- **Cleanup**: know exactly which records to delete
- **JSON export**: optional manifest for CI reports

### Usage

```python
def test_something(db_session, test_data_registry):
    condo = create_condo(name="Mi Condo Test")
    test_data_registry.register("condo", condo.id, condo.uuid)

    # ... run test ...

    # On teardown, registry knows condo.id → delete from DB
```

---

## Cleanup Strategy

### Per-Test Cleanup

If a test uses transactions, rollback after each test:

```python
@pytest.fixture
def db_session(test_db_connection):
    with test_db_connection.begin():
        yield test_db_connection
    # Auto-rollback on exit
```

### Session-Level Cleanup (Full Reset)

At the end of the session, `teardown_test_db` drops the database:

```python
def teardown_test_db():
    with engine.connect() as conn:
        conn.execute(text("DROP DATABASE IF EXISTS db_condo_testings"))
        conn.commit()
```

### Fallback: Truncate Tables

If dropping the database is too slow or causes issues, truncate key tables:

```sql
SET FOREIGN_KEY_CHECKS = 0;
TRUNCATE TABLE core_condominiums;
TRUNCATE TABLE core_buildings;
TRUNCATE TABLE core_units;
TRUNCATE TABLE core_users;
TRUNCATE TABLE core_residents;
SET FOREIGN_KEY_CHECKS = 1;
```

---

## Module Coverage

### Phase 1 — Core Modules (Priority)

| Module | Test File | Status |
|---|---|---|
| Condominiums | `test_condo_module.py` | TODO |
| Buildings | `test_core_buildings.py` | Existing |
| Units | `test_core_unities.py` | Existing |
| Building Types | `test_core_buildings_types.py` | Existing |
| Amenities | `test_core_amenities.py` | Existing |
| RBAC | `test_core_rbac.py` | Existing |
| Users | `test_user_module.py` | TODO |
| Residents | `test_resident_module.py` | TODO |

### Phase 2 — Extended Modules

| Module | Status |
|---|---|
| Charges | TODO |
| Payments | TODO |
| Receipts | TODO |
| Ledger Entries | TODO |
| Documents | TODO |
| Announcements | TODO |
| Meetings | TODO |
| Votes | TODO |
| Incidents | TODO |
| Visitors | TODO |

---

## Git Workflow

### Branch Strategy

All testing infrastructure work happens on **`feature/test-infra-db-condo-testings`**.

```
main ←───────────────────────────── feature/test-infra-db-condo-testings
       ↖ commits (testing-infra)
```

### Commit Convention

Follows `type(scope): subject` format per `MEMORY.md`:

```
feat(testing): add db_condo_testings infrastructure

- add .env.test (gitignored)
- add conftest.py session fixtures (setup/teardown)
- add test_data_registry for ID/UUID tracking
- add factories for condo, building, unit, user, resident
- add scenario_builder.py for complete test scenarios
- document test setup, flow, and cleanup strategy
```

### Push & Merge

```bash
git push origin feature/test-infra-db-condo-testings
# Open PR → review → merge to main
```

---

## Common Tasks

### Run tests locally

```bash
# With docker compose (mysql must be running)
docker-compose -p condopy up -d mysql

# Run tests
cd src && pytest ../tests/ -v

# Run specific module
cd src && pytest ../tests/test_core_buildings.py -v
```

### Create DB manually

```bash
mysql -h mysql -u root -p123456 -e "CREATE DATABASE IF NOT EXISTS db_condo_testings;"
```

### Run migrations manually

```bash
cd src
export $(cat ../.env.test | grep -v '^#' | xargs)
alembic upgrade head
```

### Drop test DB

```bash
mysql -h mysql -u root -p123456 -e "DROP DATABASE IF EXISTS db_condo_testings;"
```

---

## FAQ

**Q: Why not use SQLite for tests?**
A: The project uses MySQL exclusively. SQLite differences (types, JSON, FK behavior) would produce false confidence.

**Q: Why not use `db_condominiums` with a test schema?**
A: Isolation. Even with a separate schema, any bug could touch production tables. A separate DB is the only true sandbox.

**Q: Why not use `pytest-django` or similar?**
A: This is a FastAPI/Pydantic/Alembic stack, not Django. The pattern here uses Alembic migrations + raw SQLAlchemy sessions.

**Q: What about parallel test execution?**
A: Not supported in Option C — the DB is created once per session. For parallel tests, use separate DB names per worker (e.g., `db_condo_testings_w1`, `db_condo_testings_w2`).

---

## File Structure

```
condo-py/
├── .env.test              # Test environment (gitignored)
├── .gitignore             # Updated to ignore .env.test
├── tests/
│   ├── conftest.py        # Session fixtures: setup/teardown
│   ├── factories/         # Data factories
│   │   ├── condo_factory.py
│   │   ├── building_factory.py
│   │   ├── unit_factory.py
│   │   ├── user_factory.py
│   │   └── resident_factory.py
│   ├── support/
│   │   ├── scenario_builder.py
│   │   └── test_data_registry.py
│   └── integration/       # Per-module integration tests
├── docs/
│   └── TESTING/
│       ├── README.md      # This file
│       ├── SETUP.md
│       ├── FLOW.md
│       └── CLEANUP.md
└── alembic/
    └── versions/          # Real migrations (source of truth for schema)
```
