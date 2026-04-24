"""
Seed script: create test condominiums.

Creates 2-3 condominios de prueba para testing del CRUD en condo-backdmin.

Usage:
  python seeds/seed_condominiums.py

Idempotent: uses SELECT → UPDATE/INSERT pattern.
"""
import pymysql
from dotenv import load_dotenv
import os

load_dotenv(os.path.join(os.path.dirname(__file__), "..", "src", ".env"))

DB_USER = os.environ.get("MYSQL_USER", "root")
DB_PASSWORD = os.environ.get("MYSQL_PASSWORD", "123456")
DB_HOST = os.environ.get("MYSQL_HOST", "mysql")
DB_PORT = os.environ.get("MYSQL_PORT", "3306")
DB_NAME = os.environ.get("MYSQL_DB", "db_condominiums")

CONDOMINIUMS = [
    {
        "code": "COSTANERA",
        "name": "Edificio Costanera",
        "description": "Torre principal de viviendas en el centro financiero.",
        "land_area": 1200.00,
        "built_area": 34813.68,
        "area_unit": "m2",
        "legal_name": "Edificio Costanera S.A.",
        "document_number": "RUC 20123456789",
        "address": "Av. Javier Prado 4567",
        "city": "Lima",
        "country": "Perú",
        "contact_email": "costanera@condominio.pe",
        "contact_phone": "+51 1 234 5678",
        "status": 1,
        "theme_id": "ocean-breeze",
    },
    {
        "code": "PALERMO",
        "name": "Residencial Palermo",
        "description": "Complejo residencial con áreas comunes.",
        "land_area": 2500.00,
        "built_area": 15200.00,
        "area_unit": "m2",
        "legal_name": "Residencial Palermo E.I.R.L.",
        "document_number": "RUC 20198765432",
        "address": "Calle Roma 234",
        "city": "Lima",
        "country": "Perú",
        "contact_email": "palermo@condominio.pe",
        "contact_phone": "+51 1 876 5432",
        "status": 1,
        "theme_id": "cyberpunk",
    },
    {
        "code": "MIRADOR",
        "name": "Torre Mirador",
        "description": "Edificio con vista al mar.",
        "land_area": 800.00,
        "built_area": 9500.00,
        "area_unit": "m2",
        "address": "Av. Costanera 890",
        "city": "Lima",
        "country": "Perú",
        "status": 1,
        "theme_id": "twitter",
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


def _exists(cursor, code: str) -> Optional[int]:
    cursor.execute(
        "SELECT id FROM core_condominiums WHERE code = %s AND deleted_at IS NULL",
        (code,),
    )
    row = cursor.fetchone()
    return row[0] if row else None


def _get_user_id(cursor, email: str) -> Optional[int]:
    cursor.execute("SELECT id FROM users WHERE email = %s", (email,))
    row = cursor.fetchone()
    return row[0] if row else None


def seed_condominiums():
    conn = _connect()
    cursor = conn.cursor()

    user_id = _get_user_id(cursor, "admin@admin.com")
    if not user_id:
        print("⚠️  User admin@admin.com not found — run seed_test_user.py first")
        conn.close()
        return

    for condo in CONDOMINIUMS:
        existing_id = _exists(cursor, condo["code"])

        if existing_id:
            # Update existing
            sets = []
            vals = []
            for field in [
                "name", "description", "land_area", "built_area", "area_unit",
                "legal_name", "document_number", "address", "city", "country",
                "contact_email", "contact_phone", "status", "theme_id",
            ]:
                if condo.get(field) is not None:
                    sets.append(f"{field} = %s")
                    vals.append(condo[field])
            if sets:
                vals.append(existing_id)
                cursor.execute(
                    f"UPDATE core_condominiums SET {', '.join(sets)} WHERE id = %s",
                    vals,
                )
            print(f"✅ Updated existing condominio {condo['code']} (id={existing_id})")
        else:
            from datetime import datetime
            import uuid as uuid_lib

            condo_uuid = str(uuid_lib.uuid4())
            now = datetime.utcnow().isoformat()

            cursor.execute(
                """
                INSERT INTO core_condominiums
                (uuid, code, name, description, land_area, built_area, area_unit,
                 legal_name, document_number, address, city, country,
                 contact_email, contact_phone, status, theme_id,
                 created_at, updated_at)
                VALUES
                (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """,
                (
                    condo_uuid,
                    condo["code"],
                    condo["name"],
                    condo.get("description"),
                    condo.get("land_area"),
                    condo.get("built_area"),
                    condo.get("area_unit", "m2"),
                    condo.get("legal_name"),
                    condo.get("document_number"),
                    condo.get("address"),
                    condo["city"],
                    condo.get("country", "Perú"),
                    condo.get("contact_email"),
                    condo.get("contact_phone"),
                    condo.get("status", 1),
                    condo.get("theme_id"),
                    now,
                    now,
                ),
            )
            new_id = cursor.lastrowid
            print(f"✅ Created condominio {condo['code']} (id={new_id})")

    conn.close()
    print("\n🎯 Condominiums seed complete")
    print(f"   Run: GET /condominiums to verify")


if __name__ == "__main__":
    seed_condominiums()
