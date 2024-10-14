"""create users table

Revision ID: ec41587082d1
Revises: f608c4212225
Create Date: 2024-09-13 14:37:26.475465

"""
from typing import Sequence, Union

# revision identifiers, used by Alembic.
revision: str = 'ec41587082d1'
down_revision: Union[str, None] = 'f608c4212225'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

table_name = 'users'


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
