"""add table partitions for id to crop_data table

Revision ID: 430cc2e94c1e
Revises: f608c4212225
Create Date: 2024-08-13 15:59:43.481359

"""
from typing import Sequence, Union

from alembic import op

# revision identifiers, used by Alembic.
revision: str = '430cc2e94c1e'
down_revision: Union[str, None] = 'f608c4212225'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

table_name = 'crop_data'


def upgrade() -> None:
    # Add partitioning to the existing table
    op.execute("""
    ALTER TABLE crop_data
    PARTITION BY HASH(id) PARTITIONS 10;
    """)

    # Optional: Verify the partitions
    op.execute("""
    SHOW CREATE TABLE crop_data;
    """)


def downgrade() -> None:
    # Remove partitioning if rolling back
    op.execute("""
    ALTER TABLE crop_data
    REMOVE PARTITIONING;
    """)

    # Optional: Verify the partitions have been removed
    op.execute("""
    SHOW CREATE TABLE crop_data;
    """)
