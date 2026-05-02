# Cleanup Strategy

## Overview

With Option C (create per run → destroy per run), cleanup is built into the session lifecycle. This document details the exact cleanup mechanism and fallback strategies.

---

## Primary Strategy: DROP DATABASE

The simplest and most reliable cleanup is dropping the entire database:

```python
def teardown_test_db():
    with engine.connect() as conn:
        conn.execute(text("DROP DATABASE IF EXISTS db_condo_testings"))
        conn.commit()
```

**Why this works for Option C:**
- The DB is created fresh for the session
- No other process depends on it during the test run
- Drop is faster than truncating all tables
- Foreign keys are handled automatically

---

## Secondary Strategy: Transaction Rollback

For tests that use `db_session` fixture with explicit transaction:

```python
@pytest.fixture
def db_session(engine):
    # Start a transaction (not autocommit)
    with engine.begin() as conn:
        yield conn
    # No explicit commit → transaction rolls back on exit
```

**Behavior:**
- Each test runs in its own transaction
- On test exit, the transaction is rolled back
- The database state is as if the test never ran
- No explicit DELETE needed

---

## Tertiary Strategy: Truncate Tables

Used when:
- `DROP DATABASE` is too slow (large DB)
- Another process holds a connection
- CI environment doesn't allow DDL

```sql
SET FOREIGN_KEY_CHECKS = 0;
TRUNCATE TABLE core_condominiums;
TRUNCATE TABLE core_buildings;
TRUNCATE TABLE core_buildings_types;
TRUNCATE TABLE core_units;
TRUNCATE TABLE core_unit_types;
TRUNCATE TABLE core_users;
TRUNCATE TABLE core_user_profiles;
TRUNCATE TABLE core_residents;
TRUNCATE TABLE core_roles;
TRUNCATE TABLE core_role_permissions;
TRUNCATE TABLE core_condominium_roles;
TRUNCATE TABLE core_amenities;
TRUNCATE TABLE core_charges;
TRUNCATE TABLE core_charge_types;
TRUNCATE TABLE core_payments;
TRUNCATE TABLE core_receipts;
TRUNCATE TABLE core_ledger_entries;
TRUNCATE TABLE core_documents;
TRUNCATE TABLE core_announcements;
TRUNCATE TABLE core_meetings;
TRUNCATE TABLE core_votes;
TRUNCATE TABLE core_incidents;
TRUNCATE TABLE core_unit_occupancies;
TRUNCATE TABLE core_unit_ownerships;
TRUNCATE TABLE core_notifications;
TRUNCATE TABLE core_audit_logs;
TRUNCATE TABLE auth_sessions;
TRUNCATE TABLE alembic_version;
SET FOREIGN_KEY_CHECKS = 1;
```

> **Important**: Order matters due to foreign key dependencies. Truncate children before parents.

---

## Partial Cleanup (Per-Test)

When you need to clean specific records without rolling back the whole transaction:

```python
def test_something(db_session, test_data_registry):
    condo = CondoFactory.create(db_session, name="Test")
    test_data_registry.register("condo", condo.id, condo.uuid)

    # ... test logic ...

    # Explicit cleanup at end of test (rarely needed with rollback)
    db_session.execute(
        text("DELETE FROM core_condominiums WHERE id = :id"),
        {"id": condo.id}
    )
```

---

## Test Data Registry Cleanup

The registry tracks created IDs per test:

```python
class TestDataRegistry:
    def __init__(self):
        self.data = {}  # {table_name: [ids...]}

    def register(self, table, id, uuid=None):
        if table not in self.data:
            self.data[table] = []
        self.data[table].append({"id": id, "uuid": uuid})

    def cleanup(self, db_session):
        # Delete in reverse dependency order
        for table, records in reversed(list(self.data.items())):
            for record in records:
                db_session.execute(
                    text(f"DELETE FROM {table} WHERE id = :id"),
                    {"id": record["id"]}
                )
```

Usage in `conftest.py`:

```python
@pytest.fixture
def test_data_registry(db_session):
    registry = TestDataRegistry()
    yield registry
    # Cleanup after test (if not using transaction rollback)
    registry.cleanup(db_session)
```

---

## Cleanup Order for Truncate

Tables must be truncated in **dependency order** (children before parents):

```
TIER 1 (no FK dependencies, can truncate in any order):
  - core_amenities
  - core_charge_types
  - core_unit_types
  - core_occupancy_types
  - alembic_version

TIER 2 (depends on TIER 1):
  - core_condominiums
  - core_buildings_types
  - core_roles

TIER 3 (depends on TIER 2):
  - core_buildings (→ core_condominiums)
  - core_condominium_roles (→ core_condominiums, core_roles)

TIER 4 (depends on TIER 3):
  - core_units (→ core_buildings)
  - core_user_profiles (→ core_users)
  - core_role_permissions (→ core_roles)

TIER 5 (depends on TIER 4):
  - core_users
  - core_residents (→ core_users, core_units)
  - core_unit_occupancies (→ core_units)
  - core_unit_ownerships (→ core_units)

TIER 6 (depends on TIER 5):
  - core_charges (→ core_condominiums, core_units)
  - core_documents (→ core_condominiums)
  - core_announcements (→ core_condominiums)
  - core_meetings (→ core_condominiums)
  - core_votes (→ core_meetings)
  - core_incidents (→ core_condominiums)
  - core_notifications

TIER 7 (depends on TIER 6):
  - core_payments (→ core_charges)
  - core_receipts (→ core_payments)
  - core_ledger_entries (→ core_condominiums)

TIER 8 (top of chain):
  - auth_sessions (→ core_users)
```

---

## Handling Alembic Version Table

The `alembic_version` table tracks migration state. It must be handled specially:

```sql
-- Option A: Don't truncate it (let alembic manage)
-- Just run `alembic downgrade base` before truncate to clean it

-- Option B: Truncate with rest
DELETE FROM alembic_version;
```

---

## Verifying Cleanup

After teardown, verify the database is clean:

```bash
mysql -h mysql -u root -p123456 db_condo_testings -e "SHOW TABLES;"
# Expected: alembic_version only (or empty if DROP DATABASE was used)
```

Or verify no orphan records:

```sql
SELECT 'core_condominiums' as tbl, COUNT(*) as cnt FROM core_condominiums
UNION ALL
SELECT 'core_buildings', COUNT(*) FROM core_buildings
UNION ALL
SELECT 'core_units', COUNT(*) FROM core_units
UNION ALL
SELECT 'core_users', COUNT(*) FROM core_users;
```

---

## CI/CD Teardown

Always run teardown in a `finally` block or `if: always()` step:

```yaml
- name: Teardown Test DB
  if: always()
  run: |
    mysql -h mysql -u root -p123456 \
      -e "DROP DATABASE IF EXISTS db_condo_testings;"
```

This ensures the DB is cleaned up even if tests crash or timeout.

---

## Common Issues

### "Cannot drop database because it's being used by other connections"

```sql
-- Kill all connections to the DB first
SELECT CONCAT('KILL ', id, ';')
FROM INFORMATION_SCHEMA.PROCESSLIST
WHERE db = 'db_condo_testings';

-- Then drop
DROP DATABASE IF EXISTS db_condo_testings;
```

### "Table is marked as crashed"

```bash
mysqlcheck -h mysql -u root -p123456 db_condo_testings --repair
```

### "Foreign key constraint fails"

Always truncate children before parents. If still failing, temporarily disable FK checks:

```sql
SET FOREIGN_KEY_CHECKS = 0;
TRUNCATE TABLE core_residents;
SET FOREIGN_KEY_CHECKS = 1;
```
