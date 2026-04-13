"""
Seed script for core_buildings_types — base catalog (idempotent, EXISTS-then-UPDATE/INSERT).

Types:
  - RESIDENTIAL (residencial)
  - COMMERCIAL (comercial)
  - MIXED (mixto)
  - SERVICES (servicios)

This seed is idempotent:
  - Does NOT use COUNT(*) > 0
  - Does NOT rely on ON DUPLICATE KEY UPDATE (no UNIQUE on just `code` after migration 006)
  - Uses SELECT → UPDATE/INSERT pattern for true upsert behaviour
  - Safe to re-run at any time
  - Updates existing base types if name/description changed

Run manually: python seeds/seed_core_buildings_types.py
"""
import uuid
from datetime import datetime
from typing import Optional, Dict, Any

import pymysql
from dotenv import load_dotenv
import os

load_dotenv(os.path.join(os.path.dirname(__file__), "..", "src", ".env"))

DB_USER = os.environ.get("MYSQL_USER", "root")
DB_PASSWORD = os.environ.get("MYSQL_PASSWORD", "123456")
DB_HOST = os.environ.get("MYSQL_HOST", "mysql")
DB_PORT = os.environ.get("MYSQL_PORT", "3306")
DB_NAME = os.environ.get("MYSQL_DB", "db_condominiums")

BASE_TYPES = [
    {
        "code": "RESIDENTIAL",
        "name": "Residencial",
        "description": (
            "Edificio de uso predominantemente residencial. "
            "Viviendas individuales o departamentos."
        ),
    },
    {
        "code": "COMMERCIAL",
        "name": "Comercial",
        "description": (
            "Edificio de uso comercial. "
            "Oficinas, locales o espacios de negocio."
        ),
    },
    {
        "code": "MIXED",
        "name": "Mixto",
        "description": (
            "Edificio con combinación de usos residenciales "
            "y comerciales en la misma estructura."
        ),
    },
    {
        "code": "SERVICES",
        "name": "Servicios",
        "description": (
            "Edificio destinado a prestación de servicios. "
            "Clínicas, universidades, centros de datos, etc."
        ),
    },
]


def _find_existing(
    cursor,
    code: str,
) -> Optional[Dict[str, Any]]:
    """
    Find an existing global building type by code.

    Uses the index on (condominium_id, code) from migration 006.
    Matches only active, non-deleted records where condominium_id IS NULL.
    """
    cursor.execute(
        """
        SELECT id, uuid, code, name, description,
               is_system, sort_order, status, created_at, updated_at
        FROM core_buildings_types
        WHERE code = %s
          AND condominium_id IS NULL
          AND deleted_at IS NULL
        LIMIT 1
        """,
        (code,),
    )
    row = cursor.fetchone()
    if not row:
        return None
    return {
        "id": row[0],
        "uuid": row[1],
        "code": row[2],
        "name": row[3],
        "description": row[4],
        "is_system": row[5],
        "sort_order": row[6],
        "status": row[7],
        "created_at": row[8],
        "updated_at": row[9],
    }


def seed_building_types() -> None:
    """
    Seed base building types with true idempotent upsert.

    Strategy (avoids ON DUPLICATE KEY UPDATE which requires a UNIQUE on `code` alone):
      1. SELECT to find existing global type by code
      2. If found: UPDATE name, description (keep UUID, created_at, id)
      3. If not found: INSERT new record

    This works correctly regardless of whether migration 006 has run.
    """
    connection = pymysql.connect(
        host=DB_HOST,
        port=int(DB_PORT),
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME,
        charset="utf8mb4",
    )

    try:
        with connection.cursor(pymysql.cursors.DictCursor) as cursor:
            updated = 0
            inserted = 0

            for bt in BASE_TYPES:
                existing = _find_existing(cursor, bt["code"])

                if existing:
                    # Update existing record: preserve UUID, id, created_at
                    # Only update name, description, is_system, sort_order, status
                    cursor.execute(
                        """
                        UPDATE core_buildings_types
                        SET name        = %s,
                            description = %s,
                            is_system   = 1,
                            sort_order  = 0,
                            status      = 1,
                            updated_at  = %s
                        WHERE id = %s
                        """,
                        (
                            bt["name"],
                            bt["description"],
                            datetime.utcnow(),
                            existing["id"],
                        ),
                    )
                    updated += 1
                    action = "UPDATE"
                else:
                    # Insert new global system type
                    cursor.execute(
                        """
                        INSERT INTO core_buildings_types
                          (uuid, code, name, description,
                           is_system, sort_order, status,
                           created_at, updated_at)
                        VALUES
                          (%s, %s, %s, %s, 1, 0, 1, %s, %s)
                        """,
                        (
                            str(uuid.uuid4()),
                            bt["code"],
                            bt["name"],
                            bt["description"],
                            datetime.utcnow(),
                            datetime.utcnow(),
                        ),
                    )
                    inserted += 1
                    action = "INSERT"

                print(f"  [{action}] {bt['code']}: {bt['name']}")

            connection.commit()
            total = updated + inserted
            print(
                f"\n✅ Seed complete."
                f"  Updated: {updated}  Inserted: {inserted}  Total: {total}"
            )
            print(f"   Base types seeded: {len(BASE_TYPES)}")

    finally:
        connection.close()


if __name__ == "__main__":
    print("Seeding core_buildings_types (idempotent SELECT→UPDATE/INSERT)...\n")
    seed_building_types()
