"""
Refactorización profunda de core_unities

Cambios sobre la tabla original (001_create_initial):
  - ELIMINADO:  `type`          (redundante con unity_type_id)
  - ELIMINADO:  `size`          (renombrado a private_area con mejor precisión)
  - ELIMINADO:  `percentage`    (renombrado a coefficient con mejor precisión)
  - ELIMINADO:  `floor`         (renombrado a floor_number)
  - ELIMINADO:  UNIQUE(code) global
  - AÑADIDO:    `deleted_at`    (soft delete)
  - AÑADIDO:    `unit_number`   (renombrado de `unit`)
  - AÑADIDO:    `private_area`  (renombrado de `size`, DECIMAL(12,4))
  - AÑADIDO:    `coefficient`   (renombrado de `percentage`, DECIMAL(9,6))
  - AÑADIDO:    `floor_number`  (renombrado de `floor`)
  - AÑADIDO:    `floor_label`   (label UI: sótano, mezzanine, PH, lobby…)
  - AÑADIDO:    `occupancy_status` (vacant|occupied|reserved|maintenance|blocked)
  - AÑADIDO:    `sort_order`    (orden visual/manual)
  - AÑADIDO:    UNIQUE compuesto (building_id, unit_number)
  - AÑADIDO:    índices estratégicos

Revisión: Misato K antes de commit.

NOTA: `unit_number` es VARCHAR(50) NULL en esta migración (hereda de `unit` original).
Su constraint NOT NULL se aplica en el schema Pydantic de la capa de aplicación,
no en Alembic — para no crashear si hay nulos legacy en producción.
Proceso de limpieza de datos legacy es responsabilidad aparte.

Revision ID: 008_refactor_core_unities
Revises: 007_fix_building_type_fk_cascade
Create Date: 2026-04-14
"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa
from sqlalchemy import text


revision: str = '008_refactor_core_unities'
down_revision: Union[str, None] = '007_fix_building_type_fk_cascade'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


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


def _index_exists(index_name: str, table: str = 'core_unities') -> bool:
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


def _constraint_exists(constraint_name: str, table: str = 'core_unities') -> bool:
    result = op.get_bind().execute(
        sa.text("""
            SELECT COUNT(*)
            FROM information_schema.TABLE_CONSTRAINTS
            WHERE TABLE_SCHEMA = DATABASE()
              AND TABLE_NAME = :table
              AND CONSTRAINT_NAME = :constraint_name
        """),
        {"table": table, "constraint_name": constraint_name},
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
    # 1. Agregar deleted_at (acolchón seguro antes de tocar otras columnas)
    # ------------------------------------------------------------------
    if not _column_exists('core_unities', 'deleted_at'):
        op.add_column(
            'core_unities',
            sa.Column('deleted_at', sa.DateTime(), nullable=True),
        )

    # ------------------------------------------------------------------
    # 2. Renombrar `unit` → `unit_number`
    # ------------------------------------------------------------------
    if _column_exists('core_unities', 'unit') and not _column_exists('core_unities', 'unit_number'):
        op.execute("ALTER TABLE core_unities CHANGE COLUMN `unit` `unit_number` VARCHAR(50) NULL")

    # ------------------------------------------------------------------
    # 3. Renombrar `size` → `private_area` y cambiar tipo a DECIMAL(12,4)
    # ------------------------------------------------------------------
    if _column_exists('core_unities', 'size') and not _column_exists('core_unities', 'private_area'):
        op.execute(
            "ALTER TABLE core_unities CHANGE COLUMN `size` `private_area` DECIMAL(12,4) NULL"
        )

    # ------------------------------------------------------------------
    # 4. Renombrar `percentage` → `coefficient` y cambiar tipo a DECIMAL(9,6)
    # ------------------------------------------------------------------
    if _column_exists('core_unities', 'percentage') and not _column_exists('core_unities', 'coefficient'):
        op.execute(
            "ALTER TABLE core_unities CHANGE COLUMN `percentage` `coefficient` DECIMAL(9,6) NULL"
        )

    # ------------------------------------------------------------------
    # 5. Renombrar `floor` → `floor_number`
    # ------------------------------------------------------------------
    if _column_exists('core_unities', 'floor') and not _column_exists('core_unities', 'floor_number'):
        op.execute("ALTER TABLE core_unities CHANGE COLUMN `floor` `floor_number` INT NULL")

    # ------------------------------------------------------------------
    # 6. Agregar `floor_label` ( VARCHAR(30) )
    # ------------------------------------------------------------------
    if not _column_exists('core_unities', 'floor_label'):
        op.add_column(
            'core_unities',
            sa.Column('floor_label', sa.String(30), nullable=True),
        )

    # ------------------------------------------------------------------
    # 7. Agregar `occupancy_status` con default 'vacant'
    # ------------------------------------------------------------------
    if not _column_exists('core_unities', 'occupancy_status'):
        op.add_column(
            'core_unities',
            sa.Column(
                'occupancy_status',
                sa.String(30),
                nullable=False,
                server_default='vacant',
            ),
        )
        # Asegurar que las filas existentes tengan valor antes de alterar la nullable-ness
        # (MySQL server_default ya lo hace, pero por claridad actualizamos valores nulos)
        op.execute(
            "UPDATE core_unities SET occupancy_status = 'vacant' WHERE occupancy_status IS NULL"
        )

    # ------------------------------------------------------------------
    # 8. Agregar `sort_order`
    # ------------------------------------------------------------------
    if not _column_exists('core_unities', 'sort_order'):
        op.add_column(
            'core_unities',
            sa.Column('sort_order', sa.Integer(), nullable=False, server_default='0'),
        )

    # ------------------------------------------------------------------
    # 9. Eliminar columna `type` (redundante con unity_type_id)
    # ------------------------------------------------------------------
    if _column_exists('core_unities', 'type'):
        op.drop_column('core_unities', 'type')

    # ------------------------------------------------------------------
    # 10. Hacer `unit_number` NOT NULL
    #    (primero verificamos que no haya nulos; si los hay, no forzamos)
    # ------------------------------------------------------------------
    # El campo `unit` era NULL en la migración original. unit_number se crea
    # como VARCHAR(50) NULL. Si hay datos con unit_number NULL, no lo hacemos
    # NOT NULL a ciegas — se documenta como requerimiento de datos.
    # La constraint NOT NULL se aplica en la capa de aplicación / schema de validación.

    # ------------------------------------------------------------------
    # 11. Eliminar UNIQUE global en `code` y reemplazarla por compuesta
    # ------------------------------------------------------------------

    # 11a. Eliminar UNIQUE(code) global si existe
    if _constraint_exists('code', 'core_unities'):
        # El nombre real de la constraint puede variar. Buscarlo.
        result = conn.execute(
            sa.text("""
                SELECT CONSTRAINT_NAME
                FROM information_schema.TABLE_CONSTRAINTS
                WHERE TABLE_SCHEMA = DATABASE()
                  AND TABLE_NAME = 'core_unities'
                  AND CONSTRAINT_NAME = 'code'
                  AND CONSTRAINT_TYPE = 'UNIQUE'
                LIMIT 1
            """)
        )
        row = result.fetchone()
        if row:
            op.drop_constraint('code', 'core_unities', type_='unique')
        else:
            # Buscar por nombre generado por MySQL (e.g. code_2, code_3…)
            result2 = conn.execute(
                sa.text("""
                    SELECT CONSTRAINT_NAME
                    FROM information_schema.TABLE_CONSTRAINTS
                    WHERE TABLE_SCHEMA = DATABASE()
                      AND TABLE_NAME = 'core_unities'
                      AND CONSTRAINT_TYPE = 'UNIQUE'
                      AND CONSTRAINT_NAME LIKE '%code%'
                    LIMIT 1
                """)
            )
            row2 = result2.fetchone()
            if row2:
                op.drop_constraint(row2[0], 'core_unities', type_='unique')

    # 11b. Crear UNIQUE compuesto (building_id, unit_number)
    #      Primero verificar que no exista ya
    if not _index_exists('ux_core_unities_building_unit_number', 'core_unities'):
        op.create_index(
            'ux_core_unities_building_unit_number',
            'core_unities',
            ['building_id', 'unit_number'],
            unique=True,
        )

    # ------------------------------------------------------------------
    # 12. Crear UNIQUE compuesto (building_id, code) — solo si code no es null
    # ------------------------------------------------------------------
    if not _index_exists('ux_core_unities_building_code', 'core_unities'):
        op.create_index(
            'ux_core_unities_building_code',
            'core_unities',
            ['building_id', 'code'],
            unique=True,
        )

    # ------------------------------------------------------------------
    # 13. Índices compuestos operativos
    # ------------------------------------------------------------------
    if not _index_exists('ix_core_unities_building_status', 'core_unities'):
        op.create_index(
            'ix_core_unities_building_status',
            'core_unities',
            ['building_id', 'status'],
        )

    if not _index_exists('ix_core_unities_building_sort', 'core_unities'):
        op.create_index(
            'ix_core_unities_building_sort',
            'core_unities',
            ['building_id', 'sort_order'],
        )

    if not _index_exists('ix_core_unities_building_floor', 'core_unities'):
        op.create_index(
            'ix_core_unities_building_floor',
            'core_unities',
            ['building_id', 'floor_number'],
        )

    if not _index_exists('ix_core_unities_building_occupancy', 'core_unities'):
        op.create_index(
            'ix_core_unities_building_occupancy',
            'core_unities',
            ['building_id', 'occupancy_status'],
        )

    # ------------------------------------------------------------------
    # 14. Indices adicionales ya cubiertos por FK: building_id, unity_type_id
    # ------------------------------------------------------------------
    if not _index_exists('ix_core_unities_status', 'core_unities'):
        op.create_index('ix_core_unities_status', 'core_unities', ['status'])


# ---------------------------------------------------------------------------
# DOWNGRADE
# ---------------------------------------------------------------------------

def downgrade() -> None:
    conn = op.get_bind()

    # Eliminar índices新增
    for idx in [
        'ux_core_unities_building_unit_number',
        'ux_core_unities_building_code',
        'ix_core_unities_building_status',
        'ix_core_unities_building_sort',
        'ix_core_unities_building_floor',
        'ix_core_unities_building_occupancy',
        'ix_core_unities_status',
    ]:
        if _index_exists(idx):
            op.drop_index(idx, 'core_unities')

    # Restaurar UNIQUE global en code
    if not _constraint_exists('code', 'core_unities'):
        op.create_unique_constraint('code', 'core_unities', ['code'])

    # Revertir floor_label
    if _column_exists('core_unities', 'floor_label'):
        op.drop_column('core_unities', 'floor_label')

    # Revertir sort_order
    if _column_exists('core_unities', 'sort_order'):
        op.drop_column('core_unities', 'sort_order')

    # Revertir occupancy_status
    if _column_exists('core_unities', 'occupancy_status'):
        op.drop_column('core_unities', 'occupancy_status')

    # Revertir floor_number → floor
    if _column_exists('core_unities', 'floor_number'):
        op.execute(
            "ALTER TABLE core_unities CHANGE COLUMN `floor_number` `floor` INT NULL"
        )

    # Revertir coefficient → percentage
    if _column_exists('core_unities', 'coefficient'):
        op.execute(
            "ALTER TABLE core_unities CHANGE COLUMN `coefficient` `percentage` DECIMAL(5,2) NULL"
        )

    # Revertir private_area → size
    if _column_exists('core_unities', 'private_area'):
        op.execute(
            "ALTER TABLE core_unities CHANGE COLUMN `private_area` `size` DECIMAL(10,2) NULL"
        )

    # Revertir unit_number → unit
    if _column_exists('core_unities', 'unit_number'):
        op.execute(
            "ALTER TABLE core_unities CHANGE COLUMN `unit_number` `unit` VARCHAR(50) NULL"
        )

    # Restaurar columna type (proveniente de unity_type_id, nullable)
    if not _column_exists('core_unities', 'type'):
        op.add_column(
            'core_unities',
            sa.Column('type', sa.String(100), nullable=True),
        )

    # Eliminar deleted_at
    if _column_exists('core_unities', 'deleted_at'):
        op.drop_column('core_unities', 'deleted_at')
