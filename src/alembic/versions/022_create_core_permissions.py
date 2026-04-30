"""
Create core_permissions — catálogo estático de permisos RBAC.

Cada permiso define un recurso + acción + scope default.
No tiene FK a otras tablas — es solo un catálogo de referencia.

Seed: 30 permisos cubriendo todos los recursos del sistema.

Revision ID: 022_create_core_permissions
Revises: 021_extend_condominium_roles
Create Date: 2026-04-16
"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa


revision: str = '022_create_core_permissions'
down_revision: Union[str, None] = '021_extend_condominium_roles'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


PERMISSIONS_SEED = [
    # Condominium
    ("condominium.read",    "condominium", "read",    "condominium", "Ver datos generales del condominio"),
    ("condominium.create",  "condominium", "create",  "condominium", "Crear nuevos condominios"),
    ("condominium.update",  "condominium", "update",  "condominium", "Editar datos del condominio"),
    ("condominium.delete",  "condominium", "delete",  "global",      "Eliminar condominios (solo super_admin)"),

    # Building
    ("building.read",       "building",    "read",    "condominium", "Ver edificios del condominio"),
    ("building.create",     "building",    "create",  "condominium", "Crear edificios"),
    ("building.update",     "building",    "update",  "condominium", "Editar edificios"),
    ("building.delete",     "building",    "delete",  "global",      "Eliminar edificios (solo super_admin)"),

    # Unit
    ("unit.read",           "unit",        "read",    "unit",        "Ver datos de unidad (propietarios/inquilinos)"),
    ("unit.create",         "unit",        "create",  "condominium", "Crear unidades en el condominio"),
    ("unit.update",         "unit",        "update",  "condominium", "Editar unidades"),
    ("unit.delete",         "unit",        "delete",  "global",      "Eliminar unidades (solo super_admin)"),

    # User management
    ("user.read",           "user",        "read",    "condominium", "Ver usuarios del condominio"),
    ("user.assign_role",    "user",        "assign",  "condominium", "Asignar roles a usuarios"),

    # Role management
    ("role.read",           "role",        "read",    "condominium", "Ver roles disponibles"),
    ("role.assign",         "role",        "assign",  "condominium", "Asignar roles (no super_admin)"),

    # Finance
    ("finance.read",        "finance",     "read",    "condominium", "Ver estados financieros"),
    ("finance.approve",     "finance",     "approve", "condominium", "Aprobar gastos y presupuestos"),
    ("finance.export",      "finance",     "export",  "condominium", "Exportar reportes financieros"),
    ("finance.write",       "finance",     "write",   "condominium", "Registrar gastos y movimientos"),

    # Incidents
    ("incident.read",       "incident",    "read",    "condominium", "Ver incidentes"),
    ("incident.create",     "incident",    "create",  "unit",        "Reportar incidente (residents)"),
    ("incident.update",     "incident",    "update",  "condominium", "Actualizar estado de incidente"),

    # Maintenance
    ("maintenance.read",    "maintenance", "read",    "condominium", "Ver solicitudes de mantenimiento"),
    ("maintenance.create",  "maintenance", "create",  "unit",        "Crear solicitud de mantenimiento"),
    ("maintenance.update",  "maintenance", "update",  "condominium", "Actualizar solicitudes de mantenimiento"),

    # Announcements
    ("announcement.read",   "announcement", "read",    "condominium", "Ver anuncios del condominio"),
    ("announcement.create",  "announcement", "create",  "condominium", "Publicar anuncios"),
    ("announcement.delete", "announcement", "delete",  "condominium", "Eliminar anuncios"),

    # Visitor logs
    ("visitor_log.read",    "visitor_log",  "read",    "condominium", "Ver registro de visitantes"),
    ("visitor_log.write",   "visitor_log",  "write",   "condominium", "Registrar entradas/salidas"),
]


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


def upgrade() -> None:
    if not _table_exists('core_permissions'):
        op.create_table(
            'core_permissions',
            sa.Column('id', sa.BigInteger(), autoincrement=True, nullable=False),
            sa.Column(
                'code',
                sa.String(100),
                nullable=False,
                unique=True,
            ),
            sa.Column('resource', sa.String(50), nullable=False, index=True),
            sa.Column('action', sa.String(30), nullable=False, index=True),
            sa.Column(
                'scope_default',
                sa.String(20),
                nullable=False,
                server_default='condominium',
            ),
            sa.Column('description', sa.String(255), nullable=True),
            sa.Column(
                'created_at',
                sa.DateTime(),
                nullable=False,
                server_default=sa.text('CURRENT_TIMESTAMP'),
            ),
            sa.PrimaryKeyConstraint('id'),
            sa.Index('ix_permissions_resource_action', 'resource', 'action'),
        )

        # Seed permissions
        for code, resource, action, scope_default, description in PERMISSIONS_SEED:
            op.execute(
                f"""
                INSERT INTO core_permissions (code, resource, action, scope_default, description)
                VALUES ('{code}', '{resource}', '{action}', '{scope_default}', '{description}')
                """
            )


def downgrade() -> None:
    op.drop_table('core_permissions')
