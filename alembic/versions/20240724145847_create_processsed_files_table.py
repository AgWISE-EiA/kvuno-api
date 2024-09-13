"""create processsed files table

Revision ID: feb6bf4b7abb
Revises: 
Create Date: 2024-07-24 14:58:47.779769

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

from app.utils.migration_utils import get_integer_column_type

# revision identifiers, used by Alembic.
revision: str = 'feb6bf4b7abb'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None
table_name = 'processed_files'


def upgrade() -> None:
    # Determine the column type based on the dialect
    op.create_table(
        f"{table_name}",
        sa.Column('id', get_integer_column_type(), primary_key=True),
        sa.Column('check_sum', sa.String(100), unique=True, nullable=False),
        sa.Column('file_name', sa.String(120), unique=False, nullable=False),
        sa.Column('processed_at', sa.DateTime, server_default=sa.func.now())
    )


def downgrade() -> None:
    op.drop_table(f"{table_name}", )
