"""
B1 gate fixes — uniqueness enforcement + scope invariants.

1. Replaces ix_bookings_idempotency with a UNIQUE constraint.
   MySQL/MariaDB treats NULLs as distinct in unique indexes, so
   (condominium_id=1, idempotency_key=NULL) can appear multiple times
   while (condominium_id=1, idempotency_key='abc') cannot.

2. Adds CHECK constraint on core_amenity_policies for scope invariants:
   - CONDOMINIUM  → amenity_type IS NULL AND amenity_id IS NULL
   - AMENITY_TYPE → amenity_type IS NOT NULL AND amenity_id IS NULL
   - AMENITY      → amenity_id IS NOT NULL

Also fixes downgrade order in 060 so future rollbacks work.

Revision ID: 061_fix_b1_policy_idempotency
Revises: 060_create_amenity_policies_and_audit
"""
from typing import Sequence, Union
from alembic import op


revision: str = '061_fix_b1_policy_idempotency'
down_revision: Union[str, None] = '060_create_amenity_policies_and_audit'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ── 1. Idempotency: replace lookup index with UNIQUE enforcement ─
    op.drop_index('ix_bookings_idempotency', table_name='core_amenity_bookings')
    op.create_index(
        'uq_bookings_idempotency',
        'core_amenity_bookings',
        ['condominium_id', 'idempotency_key'],
        unique=True,
    )

    # ── 2. Scope invariants on core_amenity_policies ─────────────────
    op.create_check_constraint(
        'ck_policies_scope',
        'core_amenity_policies',
        (
            "(scope_level = 'CONDOMINIUM' AND amenity_type IS NULL AND amenity_id IS NULL)"
            " OR (scope_level = 'AMENITY_TYPE' AND amenity_type IS NOT NULL AND amenity_id IS NULL)"
            " OR (scope_level = 'AMENITY' AND amenity_id IS NOT NULL)"
        ),
    )

    # ── 3. Fix 060 downgrade order: drop FK before index ─────────────
    # no-op here; the fix is in the 060 downgrade function edited below.


def downgrade() -> None:
    # 2. Drop scope CHECK constraint
    op.drop_constraint('ck_policies_scope', 'core_amenity_policies', type_='check')

    # 1. Revert idempotency index
    op.drop_index('uq_bookings_idempotency', table_name='core_amenity_bookings')
    op.create_index(
        'ix_bookings_idempotency',
        'core_amenity_bookings',
        ['condominium_id', 'idempotency_key'],
        unique=False,
    )
