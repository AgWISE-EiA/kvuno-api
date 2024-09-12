"""Add indexes to crop_data table

Revision ID: bfdf78c29e9e
Revises: 430cc2e94c1e
Create Date: 2024-08-16 19:53:25.359221

"""
from typing import Sequence, Union

from alembic import op

# revision identifiers, used by Alembic.
revision: str = 'bfdf78c29e9e'
down_revision: Union[str, None] = '430cc2e94c1e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

table_name = 'crop_data'


def upgrade() -> None:
    op.create_index(index_name='idx_coordinates', table_name=table_name,
                    columns=['coordinates'], postgresql_using='gist')
    op.create_index('ix_crop_data_country', 'crop_data', ['country'])
    op.create_index('ix_crop_data_province', 'crop_data', ['province'])
    op.create_index('ix_crop_data_lon', 'crop_data', ['lon'])
    op.create_index('ix_crop_data_lat', 'crop_data', ['lat'])
    op.create_index('ix_crop_data_variety', 'crop_data', ['variety'])
    op.create_index('ix_crop_data_season_type', 'crop_data', ['season_type'])
    op.create_index('ix_crop_data_opt_date', 'crop_data', ['opt_date'])
    op.create_index('ix_crop_data_planting_option', 'crop_data', ['planting_option'])
    op.create_index('ix_crop_data_check_sum', 'crop_data', ['check_sum'])


def downgrade() -> None:
    op.drop_index('ix_coordinates', table_name=table_name)
    op.drop_index('ix_crop_data_country', table_name=table_name)
    op.drop_index('ix_crop_data_province', table_name=table_name)
    op.drop_index('ix_crop_data_lon', table_name=table_name)
    op.drop_index('ix_crop_data_lat', table_name=table_name)
    op.drop_index('ix_crop_data_variety', table_name=table_name)
    op.drop_index('ix_crop_data_season_type', table_name=table_name)
    op.drop_index('ix_crop_data_opt_date', table_name=table_name)
    op.drop_index('ix_crop_data_planting_option', table_name=table_name)
    op.drop_index('ix_crop_data_check_sum', table_name=table_name)
