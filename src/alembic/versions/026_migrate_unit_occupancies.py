"""
Migrate core_unit_occupancies.occupancy_type (string) -> occupancy_type_id (FK bigint).

Revision ID: 026_migrate_unit_occupancies
Revises: 025_create_core_occupancy_types
Create Date: 2026-04-23
"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa
from sqlalchemy import text


revision: str = '026_migrate_unit_occupancies'
down_revision: Union[str, None] = '025_create_core_occupancy_types'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


# Mapping from old string codes to occupancy_type IDs (from seed)
# These IDs come from the seed in 025_create_core_occupancy_types
CODE_TO_TYPE_ID = {
    "resident_owner": 1,
    "tenant": 2,
    "family_member": 3,
    "office_user": 4,
    "occasional_user": 5,
}


def upgrade() -> None:
    # First, populate the new column with correct FK ids based on code
    # This UPDATE will SET occupancy_type_id = correct id WHERE occupancy_type = code
    # For any code that doesn't match (shouldn't happen), we default to 1 (resident_owner)
    op.execute(text("""
        UPDATE core_unit_occupancies
        SET occupancy_type_id = CASE occupancy_type
            WHEN 'resident_owner' THEN 1
            WHEN 'tenant' THEN 2
            WHEN 'family_member' THEN 3
            WHEN 'office_user' THEN 4
            WHEN 'occasional_user' THEN 5
            ELSE 1
        END
        WHERE occupancy_type_id IS NULL OR occupancy_type_id = 0
    """))

    # Now add the NOT NULL constraint and FK
    # Since we just populated all rows, we can safely make it non-nullable
    op.alter_column('core_unit_occupancies', 'occupancy_type_id',
                    existing_type=sa.BigInteger(),
                    nullable=False)

    # Add FK constraint (MySQL will verify all values exist in core_occupancy_types)
    op.create_foreign_key(
        'fk_unit_occupancies_occupancy_type',
        'core_unit_occupancies', 'core_occupancy_types',
        ['occupancy_type_id'], ['id']
    )

    # Drop old string column
    op.drop_column('core_unit_occupancies', 'occupancy_type')


def downgrade() -> None:
    # Recreate string column
    op.add_column('core_unit_occupancies',
                  sa.Column('occupancy_type', sa.String(40), nullable=True))
    # Populate string codes back from the FK
    op.execute(text("""
        UPDATE core_unit_occupancies o
        JOIN core_occupancy_types t ON o.occupancy_type_id = t.id
        SET o.occupancy_type = t.code
        WHERE o.occupancy_type IS NULL
    """))
    op.alter_column('core_unit_occupancies', 'occupancy_type', nullable=False)
    # Remove FK and new column
    op.drop_constraint('fk_unit_occupancies_occupancy_type', 'core_unit_occupancies', type_='foreignkey')
    op.drop_column('core_unit_occupancies', 'occupancy_type_id')