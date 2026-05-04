"""
B1 — Policy engine foundations.

Creates:
- core_amenity_policies (typed policy table with JSON extensions)
- Extends core_amenity_bookings (guest_count, allocation metadata, idempotency, policy snapshot)
- core_amenity_allocation_audit (defensible allocation decisions)

Revision ID: 060_create_amenity_policies_and_audit
Revises: 059_seed_payment_proof_permissions
"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa


revision: str = '060_create_amenity_policies_and_audit'
down_revision: Union[str, None] = '059_seed_payment_proof_permissions'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ── 1. Create core_amenity_policies ───────────────────────────────
    op.create_table(
        'core_amenity_policies',
        # PK
        sa.Column('id', sa.BigInteger(), primary_key=True, autoincrement=True, nullable=False),

        # Scope
        sa.Column('condominium_id', sa.BigInteger(), nullable=False),
        sa.Column(
            'scope_level',
            sa.String(20),
            nullable=False,
            server_default='CONDOMINIUM',
            comment='CONDOMINIUM | AMENITY_TYPE | AMENITY',
        ),
        sa.Column(
            'amenity_type',
            sa.String(30),
            nullable=True,
            comment='POOL | GRILL | SUM | GYM | GUEST_SUITE | EVENT_ROOM | ...',
        ),
        sa.Column('amenity_id', sa.BigInteger(), nullable=True),

        # Eligibility
        sa.Column(
            'eligibility_mode',
            sa.String(30),
            nullable=False,
            server_default='all_residents',
            comment='all_residents | owner_only | good_standing_only | owner_or_tenant | admin_override',
        ),

        # Usage limits
        sa.Column('max_reservations_per_period', sa.Integer(), nullable=True),
        sa.Column(
            'period_unit',
            sa.String(10),
            nullable=True,
            comment='day | week | month | quarter',
        ),
        sa.Column('period_value', sa.Integer(), nullable=True, comment='e.g. 1, 3'),
        sa.Column('max_active_reservations', sa.Integer(), nullable=True, comment='Concurrent active per unit'),
        sa.Column('max_guests', sa.Integer(), nullable=True, comment='Max guests per booking'),

        # Priority
        sa.Column(
            'priority_policy',
            sa.String(30),
            nullable=False,
            server_default='fifo',
            comment='fifo | less_usage_first | equal_share',
        ),
        sa.Column(
            'priority_window_unit',
            sa.String(10),
            nullable=True,
            comment='month | quarter | year',
        ),
        sa.Column('priority_window_value', sa.Integer(), nullable=True, comment='e.g. 1, 3'),

        # Waitlist
        sa.Column(
            'waitlist_mode',
            sa.String(30),
            nullable=False,
            server_default='notify_and_confirm',
            comment='auto_confirm | notify_and_confirm | admin_review',
        ),

        # Approval
        sa.Column(
            'approval_mode',
            sa.String(30),
            nullable=False,
            server_default='auto',
            comment='auto | amenity_requires_approval | admin_only',
        ),

        # Edge cases
        sa.Column('extra_rules_json', sa.JSON(), nullable=True, comment='Untyped extensions for rare rules'),

        # Metadata
        sa.Column('is_active', sa.Boolean(), nullable=False, server_default='1'),
        sa.Column('version', sa.Integer(), nullable=False, server_default='1', comment='Simple versioning'),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.text('NOW()')),
        sa.Column('updated_at', sa.DateTime(), nullable=True),

        # Constraints & indexes
        sa.ForeignKeyConstraint(
            ['condominium_id'], ['core_condominiums.id'],
            name='fk_policy_condominium',
        ),
        sa.ForeignKeyConstraint(
            ['amenity_id'], ['core_amenities.id'],
            name='fk_policy_amenity',
        ),
    )

    # Scope resolution index — critical for cascade lookup
    op.create_index(
        'ix_policies_scope',
        'core_amenity_policies',
        ['condominium_id', 'scope_level', 'amenity_type', 'amenity_id', 'is_active'],
    )

    # ── 2. Extend core_amenity_bookings ───────────────────────────────
    op.add_column('core_amenity_bookings', sa.Column(
        'guest_count',
        sa.Integer(),
        nullable=False,
        server_default='1',
        comment='Actual group size (affects capacity consumption)',
    ))
    op.add_column('core_amenity_bookings', sa.Column(
        'allocation_source',
        sa.String(30),
        nullable=False,
        server_default='DIRECT',
        comment='DIRECT | WAITLIST | ADMIN_OVERRIDE',
    ))
    op.add_column('core_amenity_bookings', sa.Column(
        'waitlist_entry_id',
        sa.BigInteger(),
        nullable=True,
        comment='FK → core_amenity_waitlist (added in B6)',
    ))
    op.add_column('core_amenity_bookings', sa.Column(
        'idempotency_key',
        sa.String(64),
        nullable=True,
        comment='Client-supplied key for retry safety',
    ))
    op.add_column('core_amenity_bookings', sa.Column(
        'policy_snapshot_json',
        sa.JSON(),
        nullable=True,
        comment='EffectiveAmenityPolicy frozen at booking time',
    ))
    op.add_column('core_amenity_bookings', sa.Column(
        'allocation_reason_json',
        sa.JSON(),
        nullable=True,
        comment='Why this booking was accepted / re-assigned',
    ))

    # Index for idempotency lookups
    op.create_index(
        'ix_bookings_idempotency',
        'core_amenity_bookings',
        ['condominium_id', 'idempotency_key'],
        unique=False,
        postgresql_where=sa.text('idempotency_key IS NOT NULL'),
    )

    # ── 3. Create core_amenity_allocation_audit ───────────────────────
    op.create_table(
        'core_amenity_allocation_audit',
        sa.Column('id', sa.BigInteger(), primary_key=True, autoincrement=True, nullable=False),

        # Scope
        sa.Column('amenity_id', sa.BigInteger(), nullable=False),

        # Target (one of these will be set)
        sa.Column('booking_id', sa.BigInteger(), nullable=True),
        sa.Column('waitlist_entry_id', sa.BigInteger(), nullable=True),

        # Decision
        sa.Column(
            'decision_type',
            sa.String(30),
            nullable=False,
            comment='BOOKING_ACCEPTED | BOOKING_REJECTED | WAITLIST_INSERTED | WAITLIST_PROMOTED | WAITLIST_EXPIRED | CANCELLED',
        ),
        sa.Column(
            'decision_reason',
            sa.String(255),
            nullable=True,
            comment='Short human-readable reason',
        ),
        sa.Column(
            'decision_context_json',
            sa.JSON(),
            nullable=True,
            comment='Full snapshot: policy used, score, slot state, etc.',
        ),

        # Metadata
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.text('NOW()')),

        # FK constraints
        sa.ForeignKeyConstraint(
            ['amenity_id'], ['core_amenities.id'],
            name='fk_audit_amenity',
        ),
        sa.ForeignKeyConstraint(
            ['booking_id'], ['core_amenity_bookings.id'],
            name='fk_audit_booking',
        ),
    )

    # Audit query index
    op.create_index(
        'ix_allocation_audit_lookup',
        'core_amenity_allocation_audit',
        ['amenity_id', 'decision_type', 'created_at'],
    )


def downgrade() -> None:
    # 3. Drop allocation audit (FK first, then index, then table)
    op.drop_constraint('fk_audit_booking', 'core_amenity_allocation_audit', type_='foreignkey')
    op.drop_constraint('fk_audit_amenity', 'core_amenity_allocation_audit', type_='foreignkey')
    op.drop_index('ix_allocation_audit_lookup', table_name='core_amenity_allocation_audit')
    op.drop_table('core_amenity_allocation_audit')

    # 2. Revert booking extensions
    op.drop_index('ix_bookings_idempotency', table_name='core_amenity_bookings')
    op.drop_column('core_amenity_bookings', 'allocation_reason_json')
    op.drop_column('core_amenity_bookings', 'policy_snapshot_json')
    op.drop_column('core_amenity_bookings', 'idempotency_key')
    op.drop_column('core_amenity_bookings', 'waitlist_entry_id')
    op.drop_column('core_amenity_bookings', 'allocation_source')
    op.drop_column('core_amenity_bookings', 'guest_count')

    # 1. Drop policies
    op.drop_index('ix_policies_scope', table_name='core_amenity_policies')
    op.drop_table('core_amenity_policies')
