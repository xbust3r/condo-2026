"""
Create core_role_permissions — pivot que mapea rol → permisos.

Un rol tiene N permisos. Un permiso puede pertenecer a N roles.
Scope override permite例外r el scope_default del permiso.

Seed: mapeo completo de los 8 roles v1 a sus permisos.

Revision ID: 023_create_core_role_permissions
Revises: 022_create_core_permissions
Create Date: 2026-04-16
"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa


revision: str = '023_create_core_role_permissions'
down_revision: Union[str, None] = '022_create_core_permissions'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


# (role, permission_code, scope_override)
# scope_override = NULL → usa el scope_default del permission
ROLE_PERMISSIONS_SEED = [
    # ── super_admin ──────────────────────────────────────────
    ("super_admin", "condominium.read",    None),
    ("super_admin", "condominium.create",  None),
    ("super_admin", "condominium.update",  None),
    ("super_admin", "condominium.delete",  None),
    ("super_admin", "building.read",       None),
    ("super_admin", "building.create",     None),
    ("super_admin", "building.update",     None),
    ("super_admin", "building.delete",     None),
    ("super_admin", "unit.read",           None),
    ("super_admin", "unit.create",         None),
    ("super_admin", "unit.update",         None),
    ("super_admin", "unit.delete",         None),
    ("super_admin", "user.read",           None),
    ("super_admin", "user.assign_role",    None),
    ("super_admin", "role.read",           None),
    ("super_admin", "role.assign",         None),
    ("super_admin", "finance.read",        None),
    ("super_admin", "finance.approve",     None),
    ("super_admin", "finance.export",      None),
    ("super_admin", "finance.write",       None),
    ("super_admin", "incident.read",       None),
    ("super_admin", "incident.create",     None),
    ("super_admin", "incident.update",     None),
    ("super_admin", "maintenance.read",    None),
    ("super_admin", "maintenance.create",  None),
    ("super_admin", "maintenance.update",  None),
    ("super_admin", "announcement.read",   None),
    ("super_admin", "announcement.create", None),
    ("super_admin", "announcement.delete", None),
    ("super_admin", "visitor_log.read",    None),
    ("super_admin", "visitor_log.write",   None),

    # ── condominium_admin ─────────────────────────────────────
    ("condominium_admin", "condominium.read",    None),
    ("condominium_admin", "condominium.create",  None),
    ("condominium_admin", "condominium.update",  None),
    ("condominium_admin", "building.read",       None),
    ("condominium_admin", "building.create",     None),
    ("condominium_admin", "building.update",     None),
    ("condominium_admin", "unit.read",           None),
    ("condominium_admin", "unit.create",         None),
    ("condominium_admin", "unit.update",         None),
    ("condominium_admin", "user.read",           None),
    ("condominium_admin", "user.assign_role",    None),
    ("condominium_admin", "role.read",           None),
    ("condominium_admin", "role.assign",         None),
    ("condominium_admin", "finance.read",        None),
    ("condominium_admin", "finance.write",       None),
    ("condominium_admin", "incident.read",       None),
    ("condominium_admin", "incident.create",     None),
    ("condominium_admin", "incident.update",     None),
    ("condominium_admin", "maintenance.read",    None),
    ("condominium_admin", "maintenance.create",  None),
    ("condominium_admin", "maintenance.update",  None),
    ("condominium_admin", "announcement.read",   None),
    ("condominium_admin", "announcement.create",  None),
    ("condominium_admin", "announcement.delete", None),
    ("condominium_admin", "visitor_log.read",    None),
    ("condominium_admin", "visitor_log.write",   None),

    # ── board_member ─────────────────────────────────────────
    ("board_member", "condominium.read",   None),
    ("board_member", "finance.read",      None),
    ("board_member", "finance.approve",   None),
    ("board_member", "finance.export",     None),

    # ── finance_reviewer ──────────────────────────────────────
    ("finance_reviewer", "finance.read",    None),
    ("finance_reviewer", "finance.approve", None),
    ("finance_reviewer", "finance.export",  None),
    ("finance_reviewer", "announcement.read", None),

    # ── security_staff ────────────────────────────────────────
    ("security_staff", "incident.read",      None),
    ("security_staff", "incident.create",    None),
    ("security_staff", "incident.update",    None),
    ("security_staff", "visitor_log.read",   None),
    ("security_staff", "visitor_log.write",  None),
    ("security_staff", "unit.read",          None),
    ("security_staff", "building.read",       None),

    # ── maintenance_staff ────────────────────────────────────
    ("maintenance_staff", "maintenance.read",    None),
    ("maintenance_staff", "maintenance.create",  None),
    ("maintenance_staff", "maintenance.update",  None),
    ("maintenance_staff", "building.read",        None),
    ("maintenance_staff", "unit.read",            None),

    # ── operations_staff ──────────────────────────────────────
    ("operations_staff", "announcement.read",   None),
    ("operations_staff", "announcement.create", None),
    ("operations_staff", "building.read",        None),
    ("operations_staff", "visitor_log.read",     None),
    ("operations_staff", "visitor_log.write",    None),

    # ── resident (calculado, no asignado — seed incluido para completitud) ──
    ("resident", "incident.read",       None),
    ("resident", "incident.create",     None),
    ("resident", "maintenance.read",    None),
    ("resident", "maintenance.create",  None),
    ("resident", "unit.read",           None),
    ("resident", "announcement.read",  None),
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
    if not _table_exists('core_role_permissions'):
        op.create_table(
            'core_role_permissions',
            sa.Column(
                'role',
                sa.String(40),
                nullable=False,
            ),
            sa.Column(
                'permission_code',
                sa.String(100),
                nullable=False,
            ),
            sa.Column(
                'scope_override',
                sa.String(20),
                nullable=True,
            ),
            sa.PrimaryKeyConstraint('role', 'permission_code'),
            sa.ForeignKeyConstraint(
                ['permission_code'],
                ['core_permissions.code'],
                name='fk_role_permissions_permission',
                ondelete='CASCADE',
            ),
            sa.Index('ix_role_permissions_role', 'role'),
        )

        # Seed
        for role, permission_code, scope_override in ROLE_PERMISSIONS_SEED:
            override_sql = "NULL" if scope_override is None else f"'{scope_override}'"
            op.execute(
                f"""
                INSERT INTO core_role_permissions (role, permission_code, scope_override)
                VALUES ('{role}', '{permission_code}', {override_sql})
                """
            )


def downgrade() -> None:
    op.drop_table('core_role_permissions')
