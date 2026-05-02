# Test Setup

## Prerequisites

- Docker and Docker Compose running (`mysql` container up)
- Access to MySQL on `mysql:3306` as `root`
- `python3` and `pip` available locally (for local runs)
- `pytest` installed (`pip install pytest`)

---

## 1. Create `.env.test`

> **Note**: `.env.test` is gitignored. It is generated **once** from `src/.env` and never committed.

```bash
# Copy from src/.env and override DB name
cat src/.env | sed 's/db_condominiums/db_condo_testings/' > .env.test
```

Verify:

```bash
grep MYSQL_DB .env.test
# Expected: MYSQL_DB=db_condo_testings
```

---

## 2. Create the Test Database

### Via MySQL CLI

```bash
mysql -h mysql -u root -p123456 -e "CREATE DATABASE IF NOT EXISTS db_condo_testings;"
```

### Via Makefile (if target exists)

```bash
make create_test_db
```

---

## 3. Run Alembic Migrations

```bash
cd src
export $(grep -v '^#' ../.env.test | xargs)
alembic upgrade head
```

Expected output:

```
Running upgrade  -> 001_create_initial, ...
Running upgrade 001_create_initial -> 002_refactor_core_buildings, ...
...
```

---

## 4. Verify Schema

```bash
mysql -h mysql -u root -p123456 db_condo_testings -e "SHOW TABLES;"
```

Expected tables (at minimum):
- `core_condominiums`
- `core_buildings`
- `core_units`
- `core_users`
- `core_residents`
- `core_roles`
- `alembic_version`

---

## 5. Verify Pytest Can Connect

```bash
cd src
export PYTHONPATH=.
export $(grep -v '^#' ../.env.test | xargs)
pytest --co -q ../tests/
```

Expected: list of collected tests, no connection errors.

---

## 6. (Optional) Run a Smoke Test

```bash
cd src
export PYTHONPATH=.
export $(grep -v '^#' ../.env.test | xargs)
pytest ../tests/test_core_buildings.py -v --tb=short
```

Expected: tests pass (or fail for reasons unrelated to DB connection).

---

## Troubleshooting

### "Can't connect to MySQL server on 'mysql'"

```bash
# Check if container is running
docker ps | grep mysql

# If not, start it
docker-compose -p condopy up -d mysql
```

### "Access denied for user 'root'@'%'"

```bash
# Fix MySQL root user
docker-compose -p condopy exec mysql mysql -u root -p123456 \
  -e "ALTER USER 'root'@'%' IDENTIFIED WITH mysql_native_password BY '123456';"
```

### "No module named 'alembic'"

```bash
cd src && pip install -r requirements.txt
```

---

## Full Local Setup Script

```bash
#!/bin/bash
set -e

echo "=== 1. Creating .env.test ==="
cat src/.env | sed 's/db_condominiums/db_condo_testings/' > .env.test
echo "Done."

echo "=== 2. Creating db_condo_testings ==="
mysql -h mysql -u root -p123456 -e "CREATE DATABASE IF NOT EXISTS db_condo_testings;"
echo "Done."

echo "=== 3. Running migrations ==="
cd src
export $(grep -v '^#' ../.env.test | xargs)
alembic upgrade head
cd ..

echo "=== 4. Verifying tables ==="
mysql -h mysql -u root -p123456 db_condo_testings -e "SHOW TABLES;" | wc -l
echo "tables created."

echo "=== Setup complete ==="
```
