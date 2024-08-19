"""create crop data table

Revision ID: aa7eb765e5d3
Revises: feb6bf4b7abb
Create Date: 2024-07-25 14:51:48.084926

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

from app.utils.migration_utils import get_integer_column_type

# revision identifiers, used by Alembic.
revision: str = 'aa7eb765e5d3'
down_revision: Union[str, None] = 'feb6bf4b7abb'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

table_name = 'crop_data'


def upgrade() -> None:
    op.create_table(
        f"{table_name}",
        sa.Column('id', get_integer_column_type(), primary_key=True),
        sa.Column('coordinates', sa.String(50), nullable=True, comment='Coordinates of the crop xy'),
        sa.Column('country', sa.String(20), nullable=True),
        sa.Column('province', sa.String(20), nullable=True),
        sa.Column('lon', sa.String(10), nullable=True),
        sa.Column('lat', sa.String(10), nullable=True),
        sa.Column('variety', sa.String(20), nullable=True),
        sa.Column('season_type', sa.String(20), nullable=True),
        sa.Column('opt_date', sa.String(8), nullable=True),
        sa.Column('planting_option', sa.Integer(), nullable=True),
        sa.Column('check_sum', sa.String(100), nullable=False),
        sa.Column('created_at', sa.DateTime, server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime, server_default=sa.func.now())
    )


def downgrade() -> None:
    op.drop_table(f"{table_name}", )
