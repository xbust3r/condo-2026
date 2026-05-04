"""
Add amenity_type column to core_amenities.

Replaces keyword-based inference in PolicyResolver with a proper
typed column. Supports the AMENITY_TYPE cascade level correctly.

Revision ID: 063_add_amenity_type_column
Revises: 062_nullable_policy_override_fields
"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa


revision: str = '063_add_amenity_type_column'
down_revision: Union[str, None] = '062_nullable_policy_override_fields'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


_AMENITY_TYPE_VALUES = (
    "POOL", "GRILL", "SUM", "GYM", "GUEST_SUITE", "EVENT_ROOM",
    "SPORTS_COURT", "PLAYGROUND", "COWORKING", "PETS_AREA",
    "OTHER",
)

_KEYWORD_MAP = {
    # Spanish
    'PISCINA': 'POOL', 'PICINA': 'POOL', 'PILEta': 'POOL',
    'PARRILLA': 'GRILL', 'Parrillada': 'GRILL', 'BBQ': 'GRILL',
    'ASADOR': 'GRILL', 'BARBACOA': 'GRILL', 'CHURRASQUERA': 'GRILL',
    'SUM': 'SUM', 'SALON': 'SUM', 'SALÓN': 'SUM', 'SALA': 'SUM',
    'EVENTO': 'SUM', 'EVENTOS': 'SUM', 'REUNION': 'SUM',
    'REUNIÓN': 'SUM', 'AUDITORIO': 'SUM',
    'GIMNASIO': 'GYM', 'GYM': 'GYM', 'FITNESS': 'GYM',
    'EJERCICIO': 'GYM', 'PESAS': 'GYM', 'CARDIO': 'GYM',
    'HABITACION': 'GUEST_SUITE', 'HABITACIÓN': 'GUEST_SUITE',
    'HUESPED': 'GUEST_SUITE', 'HUÉSPED': 'GUEST_SUITE',
    'VISITANTE': 'GUEST_SUITE', 'GUEST': 'GUEST_SUITE',
    'SUITE': 'GUEST_SUITE', 'DORMITORIO': 'GUEST_SUITE',
    'CANCHA': 'SPORTS_COURT', 'FUTBOL': 'SPORTS_COURT',
    'FÚTBOL': 'SPORTS_COURT', 'TENIS': 'SPORTS_COURT',
    'SQUASH': 'SPORTS_COURT', 'BASKET': 'SPORTS_COURT',
    'VOLEY': 'SPORTS_COURT', 'VOLEIBOL': 'SPORTS_COURT',
    'DEPORTE': 'SPORTS_COURT', 'DEPORTIVO': 'SPORTS_COURT',
    'JUEGO': 'PLAYGROUND', 'NIÑO': 'PLAYGROUND', 'NIÑOS': 'PLAYGROUND',
    'INFANTIL': 'PLAYGROUND', 'INFANTILES': 'PLAYGROUND',
    'COWORK': 'COWORKING', 'COWORKING': 'COWORKING',
    'OFICINA': 'COWORKING', 'TRABAJO': 'COWORKING',
    'MASCOTA': 'PETS_AREA', 'PERRO': 'PETS_AREA', 'PERROS': 'PETS_AREA',
    # English
    'POOL': 'POOL', 'GRILL': 'GRILL',
}


def _infer_type(name: str) -> str:
    """Infer amenity_type from name using keyword matching."""
    name_upper = name.upper()
    for keyword, amenity_type in sorted(_KEYWORD_MAP.items(), key=lambda x: -len(x[0])):
        if keyword in name_upper:
            return amenity_type
    return 'OTHER'


def upgrade() -> None:
    op.add_column('core_amenities', sa.Column(
        'amenity_type',
        sa.String(30),
        nullable=True,
        comment='POOL | GRILL | SUM | GYM | GUEST_SUITE | SPORTS_COURT | PLAYGROUND | COWORKING | PETS_AREA | EVENT_ROOM | OTHER',
    ))

    # Backfill existing amenities from name heuristic
    conn = op.get_bind()
    rows = conn.execute(
        sa.text("SELECT id, name FROM core_amenities WHERE amenity_type IS NULL AND deleted_at IS NULL")
    ).fetchall()

    for row in rows:
        inferred = _infer_type(row[1])
        conn.execute(
            sa.text("UPDATE core_amenities SET amenity_type = :atype WHERE id = :aid"),
            {"atype": inferred, "aid": row[0]},
        )

    op.create_index(
        'ix_amenities_type',
        'core_amenities',
        ['condominium_id', 'amenity_type'],
    )


def downgrade() -> None:
    op.drop_index('ix_amenities_type', table_name='core_amenities')
    op.drop_column('core_amenities', 'amenity_type')
