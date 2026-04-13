"""
Seed script for core_buildings_types — base catalog

Types:
  - RESIDENTIAL (residencial)
  - COMMERCIAL (comercial)
  - MIXED (mixto)
  - SERVICES (servicios)

Run manually or via Alembic migrations after 001_create_initial.
"""
from datetime import datetime
import uuid

import pymysql
from dotenv import load_dotenv
import os

load_dotenv(os.path.join(os.path.dirname(__file__), '..', 'src', '.env'))

DB_USER = os.environ.get("MYSQL_USER", "root")
DB_PASSWORD = os.environ.get("MYSQL_PASSWORD", "123456")
DB_HOST = os.environ.get("MYSQL_HOST", "mysql")
DB_PORT = os.environ.get("MYSQL_PORT", "3306")
DB_NAME = os.environ.get("MYSQL_DB", "db_condominiums")

BUILDING_TYPES = [
    {
        "uuid": str(uuid.uuid4()),
        "code": "RESIDENTIAL",
        "name": "Residencial",
        "description": "Edificio de uso predominantemente residencial. Viviendas individuales o departamentos.",
        "status": 1,
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow(),
    },
    {
        "uuid": str(uuid.uuid4()),
        "code": "COMMERCIAL",
        "name": "Comercial",
        "description": "Edificio de uso comercial. Oficinas, locales o espacios de negocio.",
        "status": 1,
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow(),
    },
    {
        "uuid": str(uuid.uuid4()),
        "code": "MIXED",
        "name": "Mixto",
        "description": "Edificio con combinación de usos residenciales y comerciales en la misma estructura.",
        "status": 1,
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow(),
    },
    {
        "uuid": str(uuid.uuid4()),
        "code": "SERVICES",
        "name": "Servicios",
        "description": "Edificio destinado a prestación de servicios. Clínicas, universidades, centros de datos, etc.",
        "status": 1,
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow(),
    },
]


def seed_building_types():
    """Insert base building types into core_buildings_types table."""
    connection = pymysql.connect(
        host=DB_HOST,
        port=int(DB_PORT),
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME,
        charset='utf8mb4',
    )

    try:
        with connection.cursor() as cursor:
            # Check if already seeded
            cursor.execute("SELECT COUNT(*) FROM core_buildings_types")
            existing = cursor.fetchone()[0]
            if existing > 0:
                print(f"core_buildings_types already has {existing} records. Skipping seed.")
                return

            for building_type in BUILDING_TYPES:
                sql = """
                    INSERT INTO core_buildings_types
                    (uuid, code, name, description, status, created_at, updated_at)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                """
                cursor.execute(sql, (
                    building_type["uuid"],
                    building_type["code"],
                    building_type["name"],
                    building_type["description"],
                    building_type["status"],
                    building_type["created_at"],
                    building_type["updated_at"],
                ))
                print(f"Inserted: {building_type['code']} — {building_type['name']}")

            connection.commit()
            print(f"✅ Seeded {len(BUILDING_TYPES)} building types successfully.")

    finally:
        connection.close()


if __name__ == "__main__":
    print("Seeding core_buildings_types...")
    seed_building_types()