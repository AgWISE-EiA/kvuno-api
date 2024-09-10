"""Add coordinates as POINT column in crop_data table

Revision ID: 51b3b196b189
Revises: fc489038eca1
Create Date: 2024-09-10 12:33:13.070558

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op
from geoalchemy2 import Geometry

# revision identifiers, used by Alembic.
revision: str = '51b3b196b189'
down_revision: Union[str, None] = 'fc489038eca1'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

table_name = 'crop_data'


def upgrade():
    # Add a POINT column using raw SQL (MariaDB supports POINT via Geometry)
    op.add_column(table_name=table_name, column=sa.Column('coordinates', Geometry(geometry_type='POINT')))

    # Optionally, add a spatial index for efficient geographic querying
    op.execute(f"ALTER TABLE {table_name} ADD SPATIAL INDEX idx_coordinates (coordinates)")


def downgrade():
    # Remove the spatial index and POINT column
    op.execute(f"ALTER TABLE {table_name} DROP INDEX idx_coordinates")

    op.drop_column(table_name=table_name, column_name='coordinates')
