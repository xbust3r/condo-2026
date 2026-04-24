"""
Seed script: core_unit_types — global system types for all condominiums.

Creates 5 global unit type records:
  RESIDENTIAL, COMMERCIAL, PARKING, STORAGE, SERVICE

These serve as the master catalog visible to all condominiums.
Custom types per condominium are also supported but go through normal CRUD.

Usage:
  python seeds/seed_unit_types.py

Idempotent: uses SELECT → UPDATE/INSERT pattern.
Does not touch uuid, id, created_at on existing records.
"""
import pymysql
from dotenv import load_dotenv
import os
from datetime import datetime
import uuid

load_dotenv(os.path.join(os.path.dirname(__file__), "..", "src", ".env"))

DB_USER = os.environ.get("MYSQL_USER", "root")
DB_PASSWORD = os.environ.get("MYSQL_PASSWORD", "123456")
DB_HOST = os.environ.get("MYSQL_HOST", "mysql")
DB_PORT = os.environ.get("MYSQL_PORT", "3306")
DB_NAME = os.environ.get("MYSQL_DB", "db_condominiums")

UNIT_TYPES = [
    {
        "code": "RESIDENTIAL",
        "name": "Residencial",
        "description": "Unidades de vivienda permanente o temporal",
        "usage_class": "residential",
        "sort_order": 1,
        "status": 1,
        "is_system": 1,
    },
    {
        "code": "COMMERCIAL",
        "name": "Comercial",
        "description": "Locales y espacios comerciales",
        "usage_class": "commercial",
        "sort_order": 2,
        "status": 1,
        "is_system": 1,
    },
    {
        "code": "PARKING",
        "name": "Estacionamiento",
        "description": "Espacios de estacionamiento vehicular",
        "usage_class": "parking",
        "sort_order": 3,
        "status": 1,
        "is_system": 1,
    },
    {
        "code": "STORAGE",
        "name": "Depósito",
        "description": "Bodegas y espacios de almacenaje",
        "usage_class": "storage",
        "sort_order": 4,
        "status": 1,
        "is_system": 1,
    },
    {
        "code": "SERVICE",
        "name": "Servicio",
        "description": "Unidades de uso técnico o institucional",
        "usage_class": "service",
        "sort_order": 5,
        "status": 1,
        "is_system": 1,
    },
]


def _connect():
    return pymysql.connect(
        host=DB_HOST,
        port=int(DB_PORT),
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME,
        autocommit=True,
    )


def _exists_by_code(cursor, code: str):
    cursor.execute(
        "SELECT id, uuid FROM core_unit_types WHERE code = %s AND deleted_at IS NULL",
        (code,),
    )
    row = cursor.fetchone()
    return (row[0], row[1]) if row else (None, None)


def seed_unit_types():
    conn = _connect()
    cursor = conn.cursor()

    for ut in UNIT_TYPES:
        existing_id, existing_uuid = _exists_by_code(cursor, ut["code"])
        now = datetime.utcnow().isoformat()

        if existing_id:
            # Idempotent update — only touch name/description/usage_class/sort_order/status/is_system
            cursor.execute(
                """
                UPDATE core_unit_types
                SET name = %s,
                    description = %s,
                    usage_class = %s,
                    sort_order = %s,
                    status = %s,
                    is_system = %s,
                    updated_at = %s
                WHERE id = %s
                """,
                (
                    ut["name"],
                    ut["description"],
                    ut["usage_class"],
                    ut["sort_order"],
                    ut["status"],
                    ut["is_system"],
                    now,
                    existing_id,
                ),
            )
            print(f"✅ Updated {ut['code']} (id={existing_id})")
        else:
            new_uuid = str(uuid.uuid4())
            cursor.execute(
                """
                INSERT INTO core_unit_types
                (uuid, condominium_id, code, name, description, is_system,
                 sort_order, usage_class, status, created_at, updated_at)
                VALUES (%s, NULL, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """,
                (
                    new_uuid,
                    ut["code"],
                    ut["name"],
                    ut["description"],
                    ut["is_system"],
                    ut["sort_order"],
                    ut["usage_class"],
                    ut["status"],
                    now,
                    now,
                ),
            )
            new_id = cursor.lastrowid
            print(f"✅ Created {ut['code']} (id={new_id})")

    conn.close()
    print(f"\n🎯 Unit types seed complete — {len(UNIT_TYPES)} global types")


if __name__ == "__main__":
    seed_unit_types()