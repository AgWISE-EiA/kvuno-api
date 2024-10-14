"""add crop name column to crop data table

Revision ID: dc494056424d
Revises: f608c4212225
Create Date: 2024-10-14 12:44:25.778408

"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = 'dc494056424d'
down_revision: Union[str, None] = 'f608c4212225'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

table_name = 'crop_data'


def upgrade() -> None:
    # Add the new column
    op.add_column(table_name, sa.Column('crop_name', sa.String(length=20), nullable=False))


def downgrade() -> None:
    # Remove the column
    op.drop_column(table_name, 'crop_name')
