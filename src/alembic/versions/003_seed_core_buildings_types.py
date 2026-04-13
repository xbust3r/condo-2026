"""seed core_buildings_types base catalog

Revision ID: 003_seed_core_buildings_types
Revises: 002_refactor_core_buildings
Create Date: 2026-04-13

Seed data for core_buildings_types:
  - RESIDENTIAL (residencial)
  - COMMERCIAL (comercial)
  - MIXED (mixto)
  - SERVICES (servicios)

"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa

revision: str = '003_seed_core_buildings_types'
down_revision: Union[str, None] = '002_refactor_core_buildings'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Check if already seeded (idempotent)
    result = op.get_bind().execute(
        sa.text("SELECT COUNT(*) FROM core_buildings_types")
    )
    count = result.fetchone()[0]
    if count > 0:
        return  # Already seeded, skip

    # Insert base building types
    op.execute("""
        INSERT INTO core_buildings_types
        (uuid, code, name, description, status, created_at, updated_at)
        VALUES
        (UUID(), 'RESIDENTIAL', 'Residencial',
         'Edificio de uso predominantemente residencial. Viviendas individuales o departamentos.',
         1, NOW(), NOW()),
        (UUID(), 'COMMERCIAL', 'Comercial',
         'Edificio de uso comercial. Oficinas, locales o espacios de negocio.',
         1, NOW(), NOW()),
        (UUID(), 'MIXED', 'Mixto',
         'Edificio con combinación de usos residenciales y comerciales en la misma estructura.',
         1, NOW(), NOW()),
        (UUID(), 'SERVICES', 'Servicios',
         'Edificio destinado a prestacion de servicios. Clinicas, universidades, centros de datos, etc.',
         1, NOW(), NOW())
    """)


def downgrade() -> None:
    op.execute("DELETE FROM core_buildings_types WHERE code IN ('RESIDENTIAL', 'COMMERCIAL', 'MIXED', 'SERVICES')")