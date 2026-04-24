"""
Seed script: create a test user for login testing.

Creates:
  - User: admin@admin.com / 12345678 (password hashed with bcrypt)
  - UserProfile linked to the user

Usage:
  python seeds/seed_test_user.py

Idempotent: if user already exists, skips creation and updates password.
"""
from typing import Optional
from datetime import datetime
import uuid as uuid_lib

import pymysql
from dotenv import load_dotenv
import os
import bcrypt

load_dotenv(os.path.join(os.path.dirname(__file__), "..", "src", ".env"))

DB_USER = os.environ.get("MYSQL_USER", "root")
DB_PASSWORD = os.environ.get("MYSQL_PASSWORD", "123456")
DB_HOST = os.environ.get("MYSQL_HOST", "mysql")
DB_PORT = os.environ.get("MYSQL_PORT", "3306")
DB_NAME = os.environ.get("MYSQL_DB", "db_condominiums")

TEST_EMAIL = "admin@admin.com"
TEST_PASSWORD = "12345678"


def _hash_password(password: str) -> str:
    salt = bcrypt.gensalt(10)
    return bcrypt.hashpw(password.encode("utf-8"), salt).decode("utf-8")


def _user_exists(cursor, email: str) -> bool:
    cursor.execute(
        "SELECT id FROM users WHERE email = %s AND deleted_at IS NULL LIMIT 1",
        (email,),
    )
    return cursor.fetchone() is not None


def _get_user_id(cursor, email: str) -> Optional[int]:
    cursor.execute(
        "SELECT id FROM users WHERE email = %s AND deleted_at IS NULL LIMIT 1",
        (email,),
    )
    row = cursor.fetchone()
    return row[0] if row else None


def _profile_exists(cursor, user_id: int) -> bool:
    cursor.execute(
        "SELECT id FROM user_profiles WHERE user_id = %s AND deleted_at IS NULL LIMIT 1",
        (user_id,),
    )
    return cursor.fetchone() is not None


def seed_test_user() -> None:
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
            password_hash = _hash_password(TEST_PASSWORD)

            if _user_exists(cursor, TEST_EMAIL):
                # Update password (idempotent — keeps same user_id)
                user_id = _get_user_id(cursor, TEST_EMAIL)
                cursor.execute(
                    """
                    UPDATE users
                    SET password_hash = %s, status = 'active', updated_at = %s
                    WHERE id = %s
                    """,
                    (password_hash, datetime.utcnow(), user_id),
                )
                connection.commit()
                print(
                    f"ℹ️  User {TEST_EMAIL} already exists — password updated. user_id={user_id}"
                )
            else:
                # Create user
                user_uuid = str(uuid_lib.uuid4())
                cursor.execute(
                    """
                    INSERT INTO users (uuid, email, password_hash, status, created_at, updated_at)
                    VALUES (%s, %s, %s, 'active', %s, %s)
                    """,
                    (user_uuid, TEST_EMAIL, password_hash, datetime.utcnow(), datetime.utcnow()),
                )
                connection.commit()
                user_id = cursor.lastrowid
                print(f"✅ Created user {TEST_EMAIL} — user_id={user_id}")

            # Create profile if missing
            if not _profile_exists(cursor, user_id):
                profile_uuid = str(uuid_lib.uuid4())
                cursor.execute(
                    """
                    INSERT INTO user_profiles (uuid, user_id, first_name, last_name)
                    VALUES (%s, %s, %s, %s)
                    """,
                    (profile_uuid, user_id, "Admin", "User"),
                )
                connection.commit()
                print(f"✅ Created user_profiles for user_id={user_id}")
            else:
                print(f"ℹ️  user_profiles already exists for user_id={user_id}")

            print(f"\n🎯 Test credentials:")
            print(f"   email:    {TEST_EMAIL}")
            print(f"   password: {TEST_PASSWORD}")

    finally:
        connection.close()


if __name__ == "__main__":
    print(f"Seeding test user {TEST_EMAIL}...\n")
    seed_test_user()
