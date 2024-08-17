"""add colum index to crop_data table

Revision ID: f608c4212225
Revises: aa7eb765e5d3
Create Date: 2024-08-13 15:55:54.121938

"""
from typing import Sequence, Union

from alembic import op

# revision identifiers, used by Alembic.
revision: str = 'f608c4212225'
down_revision: Union[str, None] = 'aa7eb765e5d3'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

table_name = 'crop_data'


def upgrade() -> None:
    # Adding index on check_sum
    op.create_index(index_name='idx_check_sum', table_name=table_name, columns=['check_sum'])

    # Adding composite index on country and province
    op.create_index(index_name='idx_country_province', table_name=table_name, columns=['country', 'province'])


def downgrade() -> None:
    # Dropping the indexes
    op.drop_index(index_name='idx_check_sum', table_name=table_name)
    op.drop_index(index_name='idx_country_province', table_name=table_name)
