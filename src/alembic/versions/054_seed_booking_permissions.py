"""
Seed booking + amenity permissions for RBAC.

Revision ID: 054_seed_booking_permissions
Revises: 053_create_amenity_bookings
"""
from typing import Sequence, Union
from alembic import op


revision: str = '054_seed_booking_permissions'
down_revision: Union[str, None] = '053_create_amenity_bookings'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


BOOKING_PERMISSIONS = [
    # Amenities (extended — booking price + deposit fields)
    ("amenities.read",     "amenities",    "read",     "condominium", "Ver amenidades/áreas comunes"),
    ("amenities.create",   "amenities",    "create",   "condominium", "Crear amenidades"),
    ("amenities.update",   "amenities",    "update",   "condominium", "Editar amenidades"),
    ("amenities.delete",   "amenities",    "delete",   "condominium", "Eliminar amenidades"),

    # Bookings
    ("bookings.read",      "bookings",     "read",     "condominium", "Ver reservas de amenidades"),
    ("bookings.create",    "bookings",     "create",   "unit",        "Crear reservas de amenidades"),
    ("bookings.update",    "bookings",     "update",   "condominium", "Confirmar/gestionar reservas"),
    ("bookings.delete",    "bookings",     "delete",   "condominium", "Cancelar reservas"),
]


def upgrade() -> None:
    for code, resource, action, scope_default, description in BOOKING_PERMISSIONS:
        op.execute(
            f"""
            INSERT INTO core_permissions (code, resource, action, scope_default, description)
            SELECT * FROM (
                SELECT '{code}' AS code, '{resource}' AS resource, '{action}' AS action,
                       '{scope_default}' AS scope_default, "{description}" AS description
            ) AS tmp
            WHERE NOT EXISTS (
                SELECT 1 FROM core_permissions WHERE code = '{code}'
            )
            """
        )


def downgrade() -> None:
    for code, _, _, _, _ in BOOKING_PERMISSIONS:
        op.execute(
            f"DELETE FROM core_permissions WHERE code = '{code}'"
        )
