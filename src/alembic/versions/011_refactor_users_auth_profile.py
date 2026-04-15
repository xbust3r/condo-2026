"""
Bloque A — Refactor users: separates auth identity from human profile.

A1. Create user_profiles table
A2. Migrate first_name/last_name/doc_identity/phone → user_profiles
A3. Drop first_name/last_name/doc_identity/phone from users
A4. Rename password → password_hash
A5. Add deleted_at, email_verified_at, last_login_at,
    failed_login_attempts, locked_until
A6. Migrate status INT → VARCHAR with documented catalog

user_profiles is 1:1 with users (user_id UNIQUE).

Catalog for users.status (VARCHAR):
  'active'       — 1  — Cuenta activa y operable
  'inactive'    — 2  — Desactivada manualmente
  'pending'     — 3  — Pendiente de verificación de email
  'suspended'   — 4  — Suspendida temporalmente
  'locked'      — 5  — Bloqueada por intentos fallidos
  'deleted'     — 6  — Eliminada (soft-delete, vía deleted_at)

Revision ID: 011_refactor_users_auth_profile
Revises: 010_rename_core_unities_to_core_units
Create Date: 2026-04-15
"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa
from sqlalchemy import text


revision: str = '011_refactor_users_auth_profile'
down_revision: Union[str, None] = '010_rename_core_unities_to_core_units'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


# Status catalog: maps legacy INT values to new VARCHAR labels
# 'active'=1, 'inactive'=2, 'pending'=3, 'suspended'=4, 'locked'=5, 'deleted'=6
STATUS_MAP = {
    1: 'active',
    2: 'inactive',
    3: 'pending',
    4: 'suspended',
    5: 'locked',
    6: 'deleted',
}
DEFAULT_STATUS = 'active'


def _table_exists(table: str) -> bool:
    result = op.get_bind().execute(
        sa.text("""
            SELECT COUNT(*)
            FROM information_schema.TABLES
            WHERE TABLE_SCHEMA = DATABASE()
              AND TABLE_NAME = :table
        """),
        {"table": table},
    )
    return result.scalar() > 0


def _column_exists(table: str, column: str) -> bool:
    result = op.get_bind().execute(
        sa.text("""
            SELECT COUNT(*)
            FROM information_schema.COLUMNS
            WHERE TABLE_SCHEMA = DATABASE()
              AND TABLE_NAME = :table
              AND COLUMN_NAME = :column
        """),
        {"table": table, "column": column},
    )
    return result.scalar() > 0


# ---------------------------------------------------------------------------
# UPGRADE
# ---------------------------------------------------------------------------

def upgrade() -> None:
    conn = op.get_bind()

    # ------------------------------------------------------------------
    # A1 — Create user_profiles
    # ------------------------------------------------------------------
    if not _table_exists('user_profiles'):
        op.create_table(
            'user_profiles',
            sa.Column('id', sa.BigInteger(), autoincrement=True, nullable=False),
            sa.Column('uuid', sa.String(36), nullable=False, server_default=sa.text('(UUID())')),
            sa.Column('user_id', sa.BigInteger(), nullable=False, unique=True),
            sa.Column('first_name', sa.String(255), nullable=True),
            sa.Column('last_name', sa.String(255), nullable=True),
            sa.Column('doc_type', sa.String(20), nullable=True),   # DNI, PASAPORTE, etc.
            sa.Column('doc_identity', sa.String(50), nullable=True),
            sa.Column('phone', sa.String(20), nullable=True),
            sa.Column('phone_country_code', sa.String(10), nullable=True),
            sa.Column('photo_url', sa.String(500), nullable=True),
            sa.Column('birth_date', sa.Date, nullable=True),
            sa.Column('gender', sa.String(20), nullable=True),
            sa.Column('nationality', sa.String(100), nullable=True),
            sa.Column('emergency_contact_name', sa.String(255), nullable=True),
            sa.Column('emergency_contact_phone', sa.String(20), nullable=True),
            sa.Column('notes', sa.Text, nullable=True),
            sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP')),
            sa.Column('updated_at', sa.DateTime(), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP')),
            sa.Column('deleted_at', sa.DateTime(), nullable=True),
            sa.PrimaryKeyConstraint('id'),
            sa.UniqueConstraint('uuid'),
            sa.UniqueConstraint('user_id'),
            sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        )

    # ------------------------------------------------------------------
    # A2 — Migrate first_name/last_name/doc_identity/phone → user_profiles
    # ------------------------------------------------------------------
    if _table_exists('user_profiles') and _column_exists('users', 'first_name'):
        # Only migrate if user_profiles is empty (first time)
        count = conn.execute(sa.text("SELECT COUNT(*) FROM user_profiles")).scalar()
        if count == 0:
            conn.execute(
                sa.text("""
                    INSERT INTO user_profiles
                      (uuid, user_id, first_name, last_name, doc_identity, phone, created_at, updated_at)
                    SELECT
                      UUID(),
                      id,
                      first_name,
                      last_name,
                      COALESCE(doc_identity, NULL),
                      COALESCE(phone, NULL),
                      created_at,
                      updated_at
                    FROM users
                    WHERE first_name IS NOT NULL
                       OR last_name IS NOT NULL
                       OR doc_identity IS NOT NULL
                       OR phone IS NOT NULL
                """)
            )

    # ------------------------------------------------------------------
    # A3 — Drop first_name, last_name, doc_identity, phone from users
    # ------------------------------------------------------------------
    if _column_exists('users', 'first_name'):
        op.drop_column('users', 'first_name')
    if _column_exists('users', 'last_name'):
        op.drop_column('users', 'last_name')
    if _column_exists('users', 'doc_identity'):
        op.drop_column('users', 'doc_identity')
    if _column_exists('users', 'phone'):
        op.drop_column('users', 'phone')

    # ------------------------------------------------------------------
    # A4 — Rename password → password_hash
    # ------------------------------------------------------------------
    if _column_exists('users', 'password') and not _column_exists('users', 'password_hash'):
        op.execute("ALTER TABLE `users` CHANGE COLUMN `password` `password_hash` VARCHAR(255) NULL")

    # ------------------------------------------------------------------
    # A5 — Add security/account management columns
    # ------------------------------------------------------------------
    if not _column_exists('users', 'deleted_at'):
        op.add_column('users', sa.Column('deleted_at', sa.DateTime(), nullable=True))

    if not _column_exists('users', 'email_verified_at'):
        op.add_column('users', sa.Column('email_verified_at', sa.DateTime(), nullable=True))

    if not _column_exists('users', 'last_login_at'):
        op.add_column('users', sa.Column('last_login_at', sa.DateTime(), nullable=True))

    if not _column_exists('users', 'failed_login_attempts'):
        op.add_column('users', sa.Column('failed_login_attempts', sa.Integer(), nullable=False, server_default='0'))

    if not _column_exists('users', 'locked_until'):
        op.add_column('users', sa.Column('locked_until', sa.DateTime(), nullable=True))

    # ------------------------------------------------------------------
    # A6 — Migrate status INT → VARCHAR
    # ------------------------------------------------------------------
    # Step 1: add new VARCHAR column (nullable, no default yet)
    if _column_exists('users', 'status') and not _table_column_is_varchar('users', 'status'):
        if not _column_exists('users', 'status_v2'):
            op.add_column('users', sa.Column('status_v2', sa.String(20), nullable=True))

        # Step 2: backfill VARCHAR from INT using catalog
        for int_val, str_val in STATUS_MAP.items():
            conn.execute(
                sa.text("UPDATE `users` SET `status_v2` = :str_val WHERE `status` = :int_val"),
                {"int_val": int_val, "str_val": str_val},
            )

        # Step 3: set default for new inserts
        conn.execute(
            sa.text("UPDATE `users` SET `status_v2` = :default WHERE `status_v2` IS NULL"),
            {"default": DEFAULT_STATUS},
        )

        # Step 4: drop old column and rename
        op.drop_column('users', 'status')
        op.alter_column('users', 'status_v2',
                        new_column_name='status',
                        type_=sa.String(20),
                        nullable=False,
                        server_default='active')

    # Add index on status (useful for filtering active/locked users)
    if not _index_exists_on_column('users', 'status'):
        op.create_index('ix_users_status', 'users', ['status'])


def _table_column_is_varchar(table: str, column: str) -> bool:
    result = op.get_bind().execute(
        sa.text("""
            SELECT COLUMN_TYPE
            FROM information_schema.COLUMNS
            WHERE TABLE_SCHEMA = DATABASE()
              AND TABLE_NAME = :table
              AND COLUMN_NAME = :column
        """),
        {"table": table, "column": column},
    )
    row = result.fetchone()
    if not row:
        return False
    col_type = str(row[0]).lower()
    return 'varchar' in col_type or 'char' in col_type


def _index_exists_on_column(table: str, column: str) -> bool:
    result = op.get_bind().execute(
        sa.text("""
            SELECT COUNT(*)
            FROM information_schema.STATISTICS
            WHERE TABLE_SCHEMA = DATABASE()
              AND TABLE_NAME = :table
              AND COLUMN_NAME = :column
        """),
        {"table": table, "column": column},
    )
    return result.scalar() > 0


# ---------------------------------------------------------------------------
# DOWNGRADE
# ---------------------------------------------------------------------------

def downgrade() -> None:
    conn = op.get_bind()

    # ------------------------------------------------------------------
    # Revert A6: status VARCHAR → INT
    # ------------------------------------------------------------------
    if _column_exists('users', 'status') and _table_column_is_varchar('users', 'status'):
        if not _column_exists('users', 'status_int'):
            op.add_column('users', sa.Column('status_int', sa.Integer(), nullable=True))

        # Reverse map: VARCHAR → INT
        for int_val, str_val in STATUS_MAP.items():
            conn.execute(
                sa.text("UPDATE `users` SET `status_int` = :int_val WHERE `status` = :str_val"),
                {"int_val": int_val, "str_val": str_val},
            )

        op.drop_column('users', 'status')
        op.alter_column('users', 'status_int',
                        new_column_name='status',
                        type_=sa.Integer(),
                        nullable=False,
                        server_default='1')
        op.drop_index('ix_users_status', table_name='users')

    # ------------------------------------------------------------------
    # Revert A5: drop security columns
    # ------------------------------------------------------------------
    for col in ('locked_until', 'failed_login_attempts', 'last_login_at',
                'email_verified_at', 'deleted_at'):
        if _column_exists('users', col):
            op.drop_column('users', col)

    # ------------------------------------------------------------------
    # Revert A4: password_hash → password
    # ------------------------------------------------------------------
    if _column_exists('users', 'password_hash') and not _column_exists('users', 'password'):
        op.execute("ALTER TABLE `users` CHANGE COLUMN `password_hash` `password` VARCHAR(255) NULL")

    # ------------------------------------------------------------------
    # Revert A3: re-add first_name, last_name, doc_identity, phone
    # ------------------------------------------------------------------
    if not _column_exists('users', 'first_name'):
        op.add_column('users', sa.Column('first_name', sa.String(255), nullable=False,
                                         server_default=''))
    if not _column_exists('users', 'last_name'):
        op.add_column('users', sa.Column('last_name', sa.String(255), nullable=False,
                                         server_default=''))
    if not _column_exists('users', 'doc_identity'):
        op.add_column('users', sa.Column('doc_identity', sa.String(50), nullable=True))
    if not _column_exists('users', 'phone'):
        op.add_column('users', sa.Column('phone', sa.String(20), nullable=True))

    # ------------------------------------------------------------------
    # Revert A2: migrate user_profiles → users
    # ------------------------------------------------------------------
    if _column_exists('user_profiles', 'first_name') and _column_exists('users', 'first_name'):
        conn.execute(
            sa.text("""
                UPDATE users u
                JOIN user_profiles p ON u.id = p.user_id
                SET u.first_name = COALESCE(p.first_name, ''),
                    u.last_name  = COALESCE(p.last_name, ''),
                    u.doc_identity = p.doc_identity,
                    u.phone       = p.phone
                WHERE u.first_name = ''
                  OR u.last_name  = ''
                  OR u.doc_identity IS NULL
                  OR u.phone       IS NULL
            """)
        )

    # ------------------------------------------------------------------
    # Revert A1: drop user_profiles
    # ------------------------------------------------------------------
    if _table_exists('user_profiles'):
        op.drop_table('user_profiles')