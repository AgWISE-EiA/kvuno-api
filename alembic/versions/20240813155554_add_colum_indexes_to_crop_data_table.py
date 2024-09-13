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
    op.create_index(index_name='idx_coordinates', table_name=table_name,
                    columns=['coordinates'], postgresql_using='gist')
    op.create_index('idx_country', table_name=table_name, columns=['country'])
    op.create_index('idx_province', table_name=table_name, columns=['province'])
    op.create_index('idx_lon', table_name=table_name, columns=['lon'])
    op.create_index('idx_lat', table_name=table_name, columns=['lat'])
    op.create_index('idx_variety', table_name=table_name, columns=['variety'])
    op.create_index('idx_season_type', table_name=table_name, columns=['season_type'])
    op.create_index('idx_opt_date', table_name=table_name, columns=['opt_date'])
    op.create_index('idx_planting_option', table_name=table_name, columns=['planting_option'])
    op.create_index('idx_check_sum', table_name=table_name, columns=['check_sum'])


def downgrade() -> None:
    op.drop_index(index_name='idx_coordinates', table_name=table_name)
    op.drop_index(index_name='idx_country', table_name=table_name)
    op.drop_index(index_name='idx_province', table_name=table_name)
    op.drop_index(index_name='idx_lon', table_name=table_name)
    op.drop_index(index_name='idx_lat', table_name=table_name)
    op.drop_index(index_name='idx_variety', table_name=table_name)
    op.drop_index(index_name='idx_season_type', table_name=table_name)
    op.drop_index(index_name='idx_opt_date', table_name=table_name)
    op.drop_index(index_name='idx_planting_option', table_name=table_name)
    op.drop_index(index_name='idx_check_sum', table_name=table_name)
