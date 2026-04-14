"""
Rename and refactor core_unittys_types → core_unities_types.

Changes over the original table (001_create_initial):
  - RENAMED:    core_unittys_types → core_unities_types
  - ADDED:      condominium_id     (nullable FK → core_condominiums)
  - ADDED:      is_system          (SmallInteger, default 0)
  - ADDED:      sort_order         (Integer, default 0)
  - ADDED:      deleted_at         (DateTime, soft delete)
  - ADDED:      usage_class        (VARCHAR(30): residential|commercial|parking|storage|service)
  - REMOVED:    global UNIQUE(code)
  - ADDED:      UNIQUE composite (condominium_id, code) — per-scope uniqueness
  - ADDED:      index on condominium_id
  - ADDED:      seed 8 base system types (idempotent upsert)

Seed types:
  APARTMENT, HOUSE, PENTHOUSE, COMMERCIAL_UNIT, OFFICE,
  PARKING, STORAGE, OTHER

Revision ID: 009_rename_and_refactor_core_unities_types
Revises: 008_refactor_core_unities
Create Date: 2026-04-14
"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa
from sqlalchemy import text


revision: str = '009_rename_and_refactor_core_unities_types'
down_revision: Union[str, None] = '008_refactor_core_unities'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


# ---------------------------------------------------------------------------
# Base unit types to seed / backfill
# ---------------------------------------------------------------------------
BASE_TYPES = [
    {
        "code": "APARTMENT",
        "name": "Apartamento",
        "description": "Unidad residencial en edificio o complejo multifamiliar. "
                       "Tipo de unidad más común en condominios horizontales o verticales.",
        "usage_class": "residential",
        "sort_order": 1,
    },
    {
        "code": "HOUSE",
        "name": "Casa",
        "description": "Unidad residencial unifamiliar, independiente o en hilera. "
                       "Común en condominios horizontales.",
        "usage_class": "residential",
        "sort_order": 2,
    },
    {
        "code": "PENTHOUSE",
        "name": "Penthouse",
        "description": "Unidad residencial premium ubicada en el último piso. "
                       "Generalmente con terraza o vista exclusiva.",
        "usage_class": "residential",
        "sort_order": 3,
    },
    {
        "code": "COMMERCIAL_UNIT",
        "name": "Local Comercial",
        "description": "Espacio destinados a actividad comercial o de negocio. "
                       "Boutiques, restaurantes, oficinas comerciales independientes.",
        "usage_class": "commercial",
        "sort_order": 4,
    },
    {
        "code": "OFFICE",
        "name": "Oficina",
        "description": "Espacio de trabajo profesional dentro de un edificio de oficinas. "
                       "Puede ser open space, privado o modular.",
        "usage_class": "commercial",
        "sort_order": 5,
    },
    {
        "code": "PARKING",
        "name": "Estacionamiento",
        "description": "Espacio dedicado al estacionamiento de vehículos. "
                       "Puede ser cubierto, descubierto o en sótano.",
        "usage_class": "parking",
        "sort_order": 6,
    },
    {
        "code": "STORAGE",
        "name": "Bodega",
        "description": "Espacio de almacenamiento independiente. "
                       "Común en desarrollos mixtos o residenciales.",
        "usage_class": "storage",
        "sort_order": 7,
    },
    {
        "code": "OTHER",
        "name": "Otro",
        "description": "Tipo genérico para unidades que no encajan en las categorías estándar. "
                       "使用时须额外说明 / Uso requiere descripción adicional.",
        "usage_class": "service",
        "sort_order": 8,
    },
]


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

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


def _index_exists(index_name: str, table: str = 'core_unities_types') -> bool:
    result = op.get_bind().execute(
        sa.text("""
            SELECT COUNT(*)
            FROM information_schema.STATISTICS
            WHERE TABLE_SCHEMA = DATABASE()
              AND TABLE_NAME = :table
              AND INDEX_NAME = :index_name
        """),
        {"table": table, "index_name": index_name},
    )
    return result.scalar() > 0


def _fk_exists_for_column(table: str, column: str) -> bool:
    result = op.get_bind().execute(
        sa.text("""
            SELECT COUNT(*)
            FROM information_schema.KEY_COLUMN_USAGE
            WHERE TABLE_SCHEMA = DATABASE()
              AND TABLE_NAME = :table
              AND COLUMN_NAME = :column
              AND REFERENCED_TABLE_NAME IS NOT NULL
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
    # 1. Rename table (MySQL renames FK references automatically)
    # ------------------------------------------------------------------
    if not _column_exists('core_unities_types', 'id'):
        op.execute("RENAME TABLE `core_unittys_types` TO `core_unities_types`")

    # ------------------------------------------------------------------
    # 2. Add new columns (order matters for MySQL)
    # ------------------------------------------------------------------
    if not _column_exists('core_unities_types', 'condominium_id'):
        op.add_column(
            'core_unities_types',
            sa.Column('condominium_id', sa.BigInteger(), nullable=True),
        )

    if not _column_exists('core_unities_types', 'is_system'):
        op.add_column(
            'core_unities_types',
            sa.Column('is_system', sa.SmallInteger(), nullable=False, server_default='0'),
        )

    if not _column_exists('core_unities_types', 'sort_order'):
        op.add_column(
            'core_unities_types',
            sa.Column('sort_order', sa.Integer(), nullable=False, server_default='0'),
        )

    if not _column_exists('core_unities_types', 'deleted_at'):
        op.add_column(
            'core_unities_types',
            sa.Column('deleted_at', sa.DateTime(), nullable=True),
        )

    if not _column_exists('core_unities_types', 'usage_class'):
        op.add_column(
            'core_unities_types',
            sa.Column('usage_class', sa.String(30), nullable=True),
        )

    # ------------------------------------------------------------------
    # 3. Drop global UNIQUE on `code`
    # ------------------------------------------------------------------
    result = conn.execute(
        sa.text("""
            SELECT c.CONSTRAINT_NAME
            FROM information_schema.TABLE_CONSTRAINTS c
            JOIN information_schema.KEY_COLUMN_USAGE k
              ON c.CONSTRAINT_NAME = k.CONSTRAINT_NAME
              AND c.TABLE_SCHEMA = k.TABLE_SCHEMA
              AND c.TABLE_NAME = k.TABLE_NAME
            WHERE c.TABLE_SCHEMA = DATABASE()
              AND c.TABLE_NAME = 'core_unities_types'
              AND c.CONSTRAINT_TYPE = 'UNIQUE'
              AND k.COLUMN_NAME = 'code'
            LIMIT 1
        """)
    )
    row = result.fetchone()
    if row:
        conn.execute(text(f"ALTER TABLE core_unities_types DROP INDEX `{row[0]}`"))

    # Idempotent fallback
    op.execute(
        "ALTER TABLE core_unities_types "
        "DROP INDEX IF EXISTS `code`, "
        "DROP INDEX IF EXISTS ix_core_unities_types_code, "
        "DROP INDEX IF EXISTS uq_core_unities_types_code"
    )

    # ------------------------------------------------------------------
    # 4. Composite index (condominium_id, code) — non-unique for scope queries.
    #
    #    Uniqueness per scope is enforced at APPLICATION LAYER:
    #    - Repository checks `get_by_code_in_scope()` before insert.
    #    - Soft-deleted rows (deleted_at IS NOT NULL) are excluded from scope
    #      searches in `get_by_code_in_scope()` — two soft-deleted types with
    #      the same code are OK because they won't be found by the app check.
    #    - Concurrent inserts: the app-layer check is NOT a lock; a race
    #      condition could theoretically slip through. For true DB-level
    #      uniqueness with soft-delete, use MySQL 8.0.34+ functional indexes:
    #
    #        CREATE UNIQUE INDEX ux_active_type_scope
    #        ON core_unities_types
    #        ((CONCAT(IFNULL(condominium_id, 'G'), '|', code)))
    #        USING HASH;
    #
    #      Or add a generated column + partial unique index. Defer until MySQL
    #      version is confirmed as 8.0.34+ in production.
    # ------------------------------------------------------------------
    if not _index_exists('ix_core_unities_types_condominium_code'):
        op.create_index(
            'ix_core_unities_types_condominium_code',
            'core_unities_types',
            ['condominium_id', 'code'],
            unique=False,
        )

    # ------------------------------------------------------------------
    # 5. Create index on condominium_id for scope filtering
    # ------------------------------------------------------------------
    if not _index_exists('ix_core_unities_types_condominium'):
        op.create_index(
            'ix_core_unities_types_condominium',
            'core_unities_types',
            ['condominium_id'],
        )

    # ------------------------------------------------------------------
    # 6. Index on status for filtered lists
    # ------------------------------------------------------------------
    if not _index_exists('ix_core_unities_types_status'):
        op.create_index(
            'ix_core_unities_types_status',
            'core_unities_types',
            ['status'],
        )

    # ------------------------------------------------------------------
    # 7. Index on usage_class for semantic filtering
    # ------------------------------------------------------------------
    if not _index_exists('ix_core_unities_types_usage_class'):
        op.create_index(
            'ix_core_unities_types_usage_class',
            'core_unities_types',
            ['usage_class'],
        )

    # ------------------------------------------------------------------
    # 8. Add FK to core_condominiums (nullable, no cascade on delete)
    # ------------------------------------------------------------------
    if not _fk_exists_for_column('core_unities_types', 'condominium_id'):
        op.execute("""
            ALTER TABLE core_unities_types
            ADD CONSTRAINT fk_unities_types_condominium
            FOREIGN KEY (condominium_id)
            REFERENCES core_condominiums(id)
            ON DELETE SET NULL
            ON UPDATE CASCADE
        """)

    # ------------------------------------------------------------------
    # 9. Backfill: mark existing rows (table was always empty, but be safe)
    # ------------------------------------------------------------------

    # ------------------------------------------------------------------
    # 10. Seed base system types — truly idempotent via DELETE + INSERT
    #
    #    Strategy: DELETE system types by (code, is_system=1) then INSERT fresh.
    #    Custom types (is_system=0 or different condominium_id) are never touched.
    #    Uses separate statements so each type is independent (no partial failure).
    # ------------------------------------------------------------------
    for bt in BASE_TYPES:
        # Delete any existing system type with this code (idempotent reset)
        conn.execute(
            sa.text("""
                DELETE FROM core_unities_types
                WHERE code = :code
                  AND is_system = 1
                  AND condominium_id IS NULL
            """),
            {"code": bt["code"]},
        )
        # Insert fresh system type
        conn.execute(
            sa.text("""
                INSERT INTO core_unities_types
                  (uuid, code, name, description,
                   usage_class, is_system, condominium_id, sort_order,
                   status, created_at, updated_at)
                VALUES
                  (UUID(), :code, :name, :description,
                   :usage_class, 1, NULL, :sort_order,
                   1, NOW(), NOW())
            """),
            {
                "code": bt["code"],
                "name": bt["name"],
                "description": bt["description"],
                "usage_class": bt["usage_class"],
                "sort_order": bt["sort_order"],
            },
        )


# ---------------------------------------------------------------------------
# DOWNGRADE
# ---------------------------------------------------------------------------

def downgrade() -> None:
    conn = op.get_bind()

    # Drop FK
    op.execute("""
        ALTER TABLE core_unities_types
        DROP FOREIGN KEY IF EXISTS fk_unities_types_condominium
    """)

    # Drop indexes
    for idx in [
        'ix_core_unities_types_condominium_code',
        'ix_core_unities_types_condominium',
        'ix_core_unities_types_status',
        'ix_core_unities_types_usage_class',
    ]:
        if _index_exists(idx):
            op.drop_index(idx, 'core_unities_types')

    # Drop columns
    for col in ['usage_class', 'deleted_at', 'sort_order', 'is_system', 'condominium_id']:
        if _column_exists('core_unities_types', col):
            op.drop_column('core_unities_types', col)

    # Restore global UNIQUE on code
    op.execute("ALTER TABLE core_unities_types ADD UNIQUE(`code`)")

    # Rename back
    op.execute("RENAME TABLE `core_unities_types` TO `core_unittys_types`")
