from alembic import op
from sqlalchemy import Integer, BigInteger


def get_integer_column_type():
    """
    Returns the appropriate SQLAlchemy column type for the primary key based on the database dialect.
    """
    if op.get_bind().dialect.name == 'sqlite':
        return Integer
    else:
        return BigInteger
