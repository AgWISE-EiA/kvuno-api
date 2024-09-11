from typing import Any, Optional

from geoalchemy2.types import Geometry
from sqlalchemy import BigInteger, DateTime, Index, Integer, PrimaryKeyConstraint, String, UniqueConstraint, text
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
        Index('idx_country_province', 'country', 'province'),
        Index('idx_crop_data_coordinates', 'coordinates'),
        Index('ix_crop_data_check_sum', 'check_sum'),
        Index('ix_crop_data_coordinates', 'location'),
        Index('ix_crop_data_country', 'country'),
        Index('ix_crop_data_lat', 'lat'),
        Index('ix_crop_data_lon', 'lon'),
        Index('ix_crop_data_opt_date', 'opt_date'),
        Index('ix_crop_data_planting_option', 'planting_option'),
        Index('ix_crop_data_province', 'province'),
        Index('ix_crop_data_season_type', 'season_type'),
        Index('ix_crop_data_variety', 'variety')
    )

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    check_sum: Mapped[str] = mapped_column(String(100))
    location: Mapped[Optional[str]] = mapped_column(String(50), comment='Coordinates of the crop xy')
    country: Mapped[Optional[str]] = mapped_column(String(20))
    province: Mapped[Optional[str]] = mapped_column(String(20))
    lon: Mapped[Optional[str]] = mapped_column(String(10))
    lat: Mapped[Optional[str]] = mapped_column(String(10))
    variety: Mapped[Optional[str]] = mapped_column(String(20))
    season_type: Mapped[Optional[str]] = mapped_column(String(20))
    opt_date: Mapped[Optional[str]] = mapped_column(String(8))
    planting_option: Mapped[Optional[int]] = mapped_column(Integer)
    created_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime, server_default=text('now()'))
    updated_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime, server_default=text('now()'))
    coordinates: Mapped[Optional[Any]] = mapped_column(Geometry('POINT', 4326, from_text='ST_GeomFromEWKT', name='geometry'))


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
