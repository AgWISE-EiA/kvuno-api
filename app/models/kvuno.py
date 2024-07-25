from typing import Optional

from sqlalchemy import DateTime, Index, String, text
from sqlalchemy.dialects.mysql import BIGINT
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
import datetime

class Base(DeclarativeBase):
    pass


class ProcessedFiles(Base):
    __tablename__ = 'processed_files'
    __table_args__ = (
        Index('check_sum', 'check_sum', unique=True),
        Index('file_name', 'file_name', unique=True)
    )

    id: Mapped[int] = mapped_column(BIGINT(20), primary_key=True)
    file_name: Mapped[str] = mapped_column(String(50))
    check_sum: Mapped[str] = mapped_column(String(100))
    processed_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime, server_default=text('current_timestamp()'))
