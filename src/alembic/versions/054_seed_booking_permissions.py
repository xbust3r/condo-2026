"""
Seed booking + amenity permissions for RBAC.

Revision ID: 054_seed_booking_permissions
Revises: 053_create_amenity_bookings
"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa


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
            sa.text("""
                INSERT IGNORE INTO core_permissions (code, resource, action, scope_default, description)
                VALUES (:code, :resource, :action, :scope_default, :description)
            """),
            {
                "code": code,
                "resource": resource,
                "action": action,
                "scope_default": scope_default,
                "description": description,
            },
        )


def downgrade() -> None:
    codes = [p[0] for p in BOOKING_PERMISSIONS]
    op.execute(
        sa.text(
            f"DELETE FROM core_permissions WHERE code IN ({','.join([':c' + str(i) for i in range(len(codes))])})"
        ),
        {f"c{i}": code for i, code in enumerate(codes)},
    )
