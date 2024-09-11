"""rename coordinates column to location in crop_data table

Revision ID: b7563067360f
Revises: bfdf78c29e9e
Create Date: 2024-09-11 15:43:17.382272

"""
from typing import Sequence, Union
import sqlalchemy as sa
from alembic import op


# revision identifiers, used by Alembic.
revision: str = 'b7563067360f'
down_revision: Union[str, None] = 'bfdf78c29e9e'
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
