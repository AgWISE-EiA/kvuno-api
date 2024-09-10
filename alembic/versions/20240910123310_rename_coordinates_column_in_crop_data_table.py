"""rename coordinates column in crop_data table

Revision ID: fc489038eca1
Revises: fdc3e8e457b6
Create Date: 2024-09-10 12:33:10.801452

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = 'fc489038eca1'
down_revision: Union[str, None] = 'fdc3e8e457b6'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

table_name = 'crop_data'


def upgrade():
    # Rename the column 'coordinates' to 'location' in the 'crop_data' table
    op.alter_column(table_name=table_name, column_name='coordinates',
                    new_column_name='location', existing_type=sa.String(50))


def downgrade():
    # Reverse the rename, from 'location' back to 'coordinates'
    op.alter_column(table_name=table_name, column_name='location',
                    new_column_name='coordinates', existing_type=sa.String(50))
