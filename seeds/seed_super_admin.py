"""
Seed script for super_admin bootstrap assignment.

RBAC-02: super_admin NO se asigna via API — solo via seed de DB.
Este script crea la primer asignación de super_admin en el sistema.

Uso:
  python seeds/seed_super_admin.py

El script es idempotente: si el super_admin ya existe (mismo user_id),
no crea duplicado — solo informa que ya existe.

Requiere que:
  1. La tabla core_condominium_roles ya exista (migración 014+)
  2. Exista al menos 1 usuario en la tabla users (para asignar el rol)
  3. Opcionalmente un condominium_id para scope específico (NULL = global)

Por defecto crea el super_admin con user_id=1 en condominium_id=NULL (global).
"""
import uuid
from datetime import datetime

import pymysql
from dotenv import load_dotenv
import os

load_dotenv(os.path.join(os.path.dirname(__file__), "..", "src", ".env"))

DB_USER = os.environ.get("MYSQL_USER", "root")
DB_PASSWORD = os.environ.get("MYSQL_PASSWORD", "123456")
DB_HOST = os.environ.get("MYSQL_HOST", "mysql")
DB_PORT = os.environ.get("MYSQL_PORT", "3306")
DB_NAME = os.environ.get("MYSQL_DB", "db_condominiums")


def _role_exists(cursor, user_id: int) -> bool:
    cursor.execute(
        """
        SELECT COUNT(*)
        FROM core_condominium_roles
        WHERE user_id = %s
          AND role = 'super_admin'
          AND deleted_at IS NULL
        LIMIT 1
        """,
        (user_id,),
    )
    return cursor.fetchone()[0] > 0


def _user_exists(cursor, user_id: int) -> bool:
    cursor.execute("SELECT COUNT(*) FROM users WHERE id = %s LIMIT 1", (user_id,))
    return cursor.fetchone()[0] > 0


def seed_super_admin(
    user_id: int = 1,
    condominium_id: int | None = None,
    status: str = "active",
) -> None:
    """
    Seed a super_admin role assignment.

    Args:
        user_id:          ID del usuario que será super_admin
        condominium_id:   NULL = global, o un condominium_id específico
        status:           'active' (default)
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
        with connection.cursor() as cursor:
            # Verificar que el usuario exista
            if not _user_exists(cursor, user_id):
                print(
                    f"❌ Usuario id={user_id} no encontrado en tabla 'users'. "
                    f"Crear el usuario primero."
                )
                return

            # Verificar si ya existe
            if _role_exists(cursor, user_id):
                print(
                    f"ℹ️  Super_admin ya existe para user_id={user_id}. "
                    f"Sin duplicados — seed omitido."
                )
                return

            # Insertar
            cursor.execute(
                """
                INSERT INTO core_condominium_roles
                  (uuid, condominium_id, user_id, role, status, scope,
                   start_date, created_at, updated_at)
                VALUES
                  (%s, %s, %s, 'super_admin', %s, 'condominium', %s, %s, %s)
                """,
                (
                    str(uuid.uuid4()),
                    condominium_id,
                    user_id,
                    status,
                    datetime.utcnow().date(),
                    datetime.utcnow(),
                    datetime.utcnow(),
                ),
            )
            connection.commit()
            print(
                f"✅ Super_admin seedeado: user_id={user_id}, "
                f"condominium_id={condominium_id}, role=super_admin"
            )
    finally:
        connection.close()


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Seed super_admin bootstrap role")
    parser.add_argument(
        "--user-id",
        type=int,
        default=1,
        help="ID del usuario que será super_admin (default: 1)",
    )
    parser.add_argument(
        "--condominium-id",
        type=int,
        default=None,
        help="Condominium ID específico o NULL para global (default: NULL)",
    )
    args = parser.parse_args()

    print(
        f"Seeding super_admin (user_id={args.user_id}, "
        f"condominium_id={args.condominium_id})...\n"
    )
    seed_super_admin(user_id=args.user_id, condominium_id=args.condominium_id)
