"""add coordinate column as geometry in crop_data table

Revision ID: e8b2fb47a82a
Revises: b7563067360f
Create Date: 2024-09-11 15:43:41.252983

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op
from geoalchemy2 import Geometry

# revision identifiers, used by Alembic.
revision: str = 'e8b2fb47a82a'
down_revision: Union[str, None] = 'b7563067360f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

table_name = 'crop_data'


def upgrade():
    # Add a POINT column using GeoAlchemy2
    op.add_column(table_name, sa.Column('coordinates', Geometry(geometry_type='POINT', srid=4326)))

    op.create_index(index_name='idx_coordinates', table_name=table_name,
                    columns=['coordinates'], postgresql_using='gist')


def downgrade():
    # Remove the spatial index and POINT column
    op.drop_index(index_name='idx_coordinates', table_name=table_name)
    op.drop_column(table_name=table_name, column_name='coordinates')
