from typing import Optional

from sqlalchemy import DateTime, Index, String, text
from sqlalchemy.dialects.mysql import BIGINT, INTEGER
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
import datetime

class Base(DeclarativeBase):
    pass


class CropData(Base):
    __tablename__ = 'crop_data'

    id: Mapped[int] = mapped_column(BIGINT(20), primary_key=True)
    check_sum: Mapped[str] = mapped_column(String(100))
    coordinates: Mapped[Optional[str]] = mapped_column(String(50), comment='Coordinates of the crop xy')
    country: Mapped[Optional[str]] = mapped_column(String(20))
    province: Mapped[Optional[str]] = mapped_column(String(20))
    lon: Mapped[Optional[str]] = mapped_column(String(10))
    lat: Mapped[Optional[str]] = mapped_column(String(10))
    variety: Mapped[Optional[str]] = mapped_column(String(20))
    season_type: Mapped[Optional[str]] = mapped_column(String(20))
    opt_date: Mapped[Optional[str]] = mapped_column(String(8))
    planting_option: Mapped[Optional[int]] = mapped_column(INTEGER(11))
    created_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime, server_default=text('current_timestamp()'))
    updated_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime, server_default=text('current_timestamp()'))


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
