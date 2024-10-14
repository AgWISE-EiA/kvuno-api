from typing import Any, Optional

from geoalchemy2.types import Geometry
from sqlalchemy import BigInteger, DateTime, Float, Index, Integer, PrimaryKeyConstraint, String, UniqueConstraint, text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
import datetime

class Base(DeclarativeBase):
    pass


class CropData(Base):
    __tablename__ = 'crop_data'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='crop_data_pkey'),
        Index('idx_check_sum', 'check_sum'),
        Index('idx_coordinates', 'coordinates'),
        Index('idx_country', 'country'),
        Index('idx_crop_data_coordinates', 'coordinates'),
        Index('idx_lat', 'lat'),
        Index('idx_lon', 'lon'),
        Index('idx_opt_date', 'opt_date'),
        Index('idx_planting_option', 'planting_option'),
        Index('idx_province', 'province'),
        Index('idx_season_type', 'season_type'),
        Index('idx_variety', 'variety')
    )

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    coordinates: Mapped[Any] = mapped_column(Geometry('POINT', 4326, from_text='ST_GeomFromEWKT', name='geometry', nullable=False))
    check_sum: Mapped[str] = mapped_column(String(100))
    crop_name: Mapped[str] = mapped_column(String(20))
    country: Mapped[Optional[str]] = mapped_column(String(20))
    province: Mapped[Optional[str]] = mapped_column(String(20))
    lon: Mapped[Optional[float]] = mapped_column(Float)
    lat: Mapped[Optional[float]] = mapped_column(Float)
    variety: Mapped[Optional[str]] = mapped_column(String(20))
    season_type: Mapped[Optional[str]] = mapped_column(String(20))
    opt_date: Mapped[Optional[str]] = mapped_column(String(8))
    planting_option: Mapped[Optional[int]] = mapped_column(Integer)
    created_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime, server_default=text('now()'))
    updated_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime, server_default=text('now()'))


class ProcessedFiles(Base):
    __tablename__ = 'processed_files'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='processed_files_pkey'),
        UniqueConstraint('check_sum', name='processed_files_check_sum_key')
    )

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    check_sum: Mapped[str] = mapped_column(String(100))
    file_name: Mapped[str] = mapped_column(String(120))
    processed_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime, server_default=text('now()'))
