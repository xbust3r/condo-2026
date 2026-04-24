"""
Seed script: core_buildings — test buildings for condo 1 (COSTANERA).

Creates buildings with varied building_type_id, coefficient, floors, etc.

Usage:
  python seeds/seed_buildings.py

Idempotent: uses SELECT → UPDATE/INSERT pattern.
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

# Buildings for condominium_id=1 (COSTANERA)
BUILDINGS = [
    {
        "code": "TORRE_A",
        "name": "Torre A",
        "short_name": "Torre A",
        "description": "Torre principal - residential",
        "condominium_id": 1,
        "building_type_id": 1,  # RESIDENTIAL
        "built_area": 10253.62,
        "common_area": 1200.00,
        "coefficient": 1.0,
        "floors_count": 17,
        "basements_count": 2,
        "units_planned": 189,
        "sort_order": 1,
        "status": 1,
    },
    {
        "code": "TORRE_B",
        "name": "Torre B",
        "short_name": "Torre B",
        "description": "Segunda torre - residential",
        "condominium_id": 1,
        "building_type_id": 1,  # RESIDENTIAL
        "built_area": 7061.57,
        "common_area": 950.00,
        "coefficient": 1.0,
        "floors_count": 14,
        "basements_count": 1,
        "units_planned": 121,
        "sort_order": 2,
        "status": 1,
    },
    {
        "code": "LOCAL_COMERCIAL",
        "name": "Local Comercial",
        "short_name": "Local",
        "description": "Área comercial en piso 1",
        "condominium_id": 1,
        "building_type_id": 2,  # COMMERCIAL
        "built_area": 850.00,
        "common_area": 80.00,
        "coefficient": 0.5,
        "floors_count": 1,
        "basements_count": 0,
        "units_planned": 5,
        "sort_order": 3,
        "status": 1,
    },
    {
        "code": "SOTANO_EST",
        "name": "Sótano Estacionamiento",
        "short_name": "Sótano",
        "description": "Solo estacionamiento",
        "condominium_id": 1,
        "building_type_id": 4,  # SERVICES
        "built_area": 2500.00,
        "common_area": 0.00,
        "coefficient": 0.0,
        "floors_count": 0,
        "basements_count": 3,
        "units_planned": 0,
        "sort_order": 4,
        "status": 1,
    },
    {
        "code": "MIXED_01",
        "name": "Bloque Mixto",
        "short_name": "Mixto",
        "description": "pisos residential + первого floor commercial",
        "condominium_id": 1,
        "building_type_id": 3,  # MIXED
        "built_area": 4500.00,
        "common_area": 600.00,
        "coefficient": 0.75,
        "floors_count": 10,
        "basements_count": 1,
        "units_planned": 80,
        "sort_order": 5,
        "status": 1,
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


def _exists(cursor, code: str, condominium_id: int):
    cursor.execute(
        "SELECT id FROM core_buildings WHERE code = %s AND condominium_id = %s AND deleted_at IS NULL",
        (code, condominium_id),
    )
    row = cursor.fetchone()
    return row[0] if row else None


def seed_buildings():
    conn = _connect()
    cursor = conn.cursor()

    for building in BUILDINGS:
        existing_id = _exists(cursor, building["code"], building["condominium_id"])
        now = datetime.utcnow().isoformat()

        if existing_id:
            sets = []
            vals = []
            for field in [
                "name", "short_name", "description", "building_type_id",
                "built_area", "common_area", "coefficient", "floors_count",
                "basements_count", "units_planned", "sort_order", "status",
            ]:
                if building.get(field) is not None:
                    sets.append(f"{field} = %s")
                    vals.append(building[field])
            if sets:
                vals.append(existing_id)
                cursor.execute(
                    f"UPDATE core_buildings SET {', '.join(sets)}, updated_at = %s WHERE id = %s",
                    vals + [now, existing_id],
                )
            print(f"✅ Updated {building['code']} (id={existing_id})")
        else:
            building_uuid = str(uuid.uuid4())
            cursor.execute(
                """
                INSERT INTO core_buildings
                (uuid, condominium_id, building_type_id, code, name, short_name,
                 description, built_area, common_area, coefficient,
                 floors_count, basements_count, units_planned, sort_order, status,
                 created_at, updated_at)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """,
                (
                    building_uuid,
                    building["condominium_id"],
                    building.get("building_type_id"),
                    building["code"],
                    building["name"],
                    building.get("short_name"),
                    building.get("description"),
                    building.get("built_area"),
                    building.get("common_area"),
                    building.get("coefficient"),
                    building["floors_count"],
                    building["basements_count"],
                    building["units_planned"],
                    building["sort_order"],
                    building["status"],
                    now,
                    now,
                ),
            )
            new_id = cursor.lastrowid
            print(f"✅ Created {building['code']} (id={new_id})")

    conn.close()
    print(f"\n🎯 Buildings seed complete — {len(BUILDINGS)} buildings for condo 1")


if __name__ == "__main__":
    seed_buildings()