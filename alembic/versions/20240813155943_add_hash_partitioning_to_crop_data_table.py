"""add table partitions for id to crop_data table

Revision ID: 430cc2e94c1e
Revises: f608c4212225
Create Date: 2024-08-13 15:59:43.481359

"""
from typing import Sequence, Union

# revision identifiers, used by Alembic.
revision: str = '430cc2e94c1e'
down_revision: Union[str, None] = 'f608c4212225'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

table_name = 'crop_data'


def upgrade() -> None:
    pass

def downgrade() -> None:
    pass