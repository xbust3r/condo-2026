# Test Flow

## Overview

This document describes the lifecycle of a test run: from database creation to teardown.

---

## Full Test Lifecycle

```
┌─────────────────────────────────────────────────────┐
│  1. SESSION START                                   │
│     - conftest.py: setup_test_db                    │
│     - Create db_condo_testings                      │
│     - Run alembic upgrade head                      │
└──────────────────────┬──────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────┐
│  2. PER-MODULE TESTS                                │
│                                                     │
│  Module: test_condo_module.py                      │
│     - fixtures: db_session, test_data_registry     │
│     - factories: create condo                      │
│     - scenario_builder: full scenario              │
│     - assertions                                   │
│     - rollback on exit                             │
│                                                     │
│  Module: test_core_buildings.py                    │
│     - (same pattern)                               │
│                                                     │
│  ... more modules ...                             │
└──────────────────────┬──────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────┐
│  3. SESSION TEARDOWN                                │
│     - conftest.py: teardown_test_db                 │
│     - DROP DATABASE db_condo_testings               │
└─────────────────────────────────────────────────────┘
```

---

## Session Fixtures (conftest.py)

### `setup_test_db` — session scope

Runs **once** at the start of the session.

```python
@pytest.fixture(scope="session", autouse=True)
def setup_test_db():
    # 1. Create DB
    create_database("db_condo_testings")
    # 2. Run migrations
    run_alembic_migrations("db_condo_testings")
    # 3. Yield → tests run
    yield
    # 4. Teardown happens in teardown_test_db
```

### `teardown_test_db` — session scope

Runs **once** at the end of the session.

```python
@pytest.fixture(scope="session", autouse=True)
def teardown_test_db():
    yield
    # DROP DATABASE db_condo_testings
    drop_database("db_condo_testings")
```

### `db_session` — function scope

Provides a transaction-wrapped session per test. Rolls back automatically.

```python
@pytest.fixture
def db_session(engine):
    with engine.begin() as conn:
        yield conn
    # Transaction auto-rollbacks on exit
```

---

## Test Function Pattern

```python
def test_create_building(db_session, test_data_registry):
    """
    1. Setup: use factory or scenario builder
    2. Act: call the actual module/service
    3. Assert: verify results
    4. Register: track created IDs for cleanup
    """
    # Step 1: Create scenario
    condo = CondoFactory.create(db_session, name="Mi Condo")
    test_data_registry.register("condo", condo.id, condo.uuid)

    building = BuildingFactory.create(
        db_session,
        condominium_id=condo.id,
        code="BLD-A",
        name="Torre A"
    )
    test_data_registry.register("building", building.id, building.uuid)

    # Step 2: Act
    result = BuildingService.get_by_id(building.id)

    # Step 3: Assert
    assert result.name == "Torre A"
    assert result.condominium_id == condo.id

    # Step 4: Registration means teardown knows what to clean
    # (but with rollback, this is mostly for debugging/audit)
```

---

## Factory Pattern

Factories wrap entity creation with sensible defaults:

```python
# Simple usage
condo = CondoFactory.create(session, name="Las Lomas")

# With overrides
condo = CondoFactory.create(
    session,
    name="Las Lomas",
    address="Av. Javier Prado 1234",
    coefficient=Decimal("100.0000")
)
```

### Available Factories

| Factory | Creates | Required Fields |
|---|---|---|
| `CondoFactory` | CondominiumEntity | `name` |
| `BuildingFactory` | BuildingEntity | `condominium_id`, `code` |
| `UnitFactory` | UnityEntity | `building_id`, `unit_number` |
| `UserFactory` | UserEntity | `email`, `document_number` |
| `ResidentFactory` | ResidentEntity | `user_id`, `unit_id` |

---

## Scenario Builder Pattern

For tests that need multiple related entities:

```python
def test_generate_charges_for_condo(db_session):
    # Creates: condo + 2 buildings + 6 units + 3 residents
    scenario = create_full_condo_scenario(
        session,
        condo_name="Torre Bonita",
        buildings_count=2,
        units_per_building=3,
        residents_per_unit=1
    )

    test_data_registry.register_scenario(scenario)

    # All related IDs are tracked
    assert len(scenario.building_ids) == 2
    assert len(scenario.unit_ids) == 6
    assert len(scenario.resident_ids) == 3

    # Run the actual test
    charges = ChargeService.generate_for_condo(scenario.condo_id)
    assert len(charges) > 0
```

---

## Test Order (Recommended)

Run modules in dependency order:

```
1. test_condo_module.py       # Base — everything belongs to a condo
2. test_core_buildings.py    # Buildings belong to a condo
3. test_core_unities.py      # Units belong to a building
4. test_core_rbac.py         # Roles/permissions reference condos
5. test_user_module.py       # Users are assigned to condos
6. test_resident_module.py   # Residents link users + units
7. test_charge_module.py     # Charges depend on condos + units
8. test_payment_module.py    # Payments depend on charges
9. test_receipt_module.py    # Receipts depend on payments
...
```

---

## What Happens on Failure

### Test Fails mid-execution

- The `db_session` fixture rolls back the transaction automatically
- No data persists from that test
- Next test sees a clean database (migrations already applied)

### Session Crashes

- `db_condo_testings` may be left dangling
- Next run: `teardown_test_db` recreates it from scratch
- Manual cleanup if needed:

```bash
mysql -h mysql -u root -p123456 -e "DROP DATABASE IF EXISTS db_condo_testings;"
```

---

## CI Flow

```yaml
# .github/workflows/test.yml (example)
- name: Setup Test DB
  run: |
    mysql -h mysql -u root -p123456 -e "CREATE DATABASE IF NOT EXISTS db_condo_testings;"

- name: Run Migrations
  run: |
    cd src
    alembic upgrade head
  env:
    MYSQL_DB: db_condo_testings

- name: Run Tests
  run: |
    cd src
    pytest ../tests/ -v --junitxml=report.xml
  env:
    PYTHONPATH: .
    MYSQL_DB: db_condo_testings

- name: Teardown
  if: always()
  run: |
    mysql -h mysql -u root -p123456 -e "DROP DATABASE IF EXISTS db_condo_testings;"
```

---

## Exit Codes

| Exit Code | Meaning |
|---|---|
| 0 | All tests passed |
| 1 | One or more tests failed |
| 2 | Test execution was interrupted |
| 3 | Internal error (e.g., fixture setup failed) |
