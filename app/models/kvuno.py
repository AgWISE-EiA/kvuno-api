import datetime
from typing import Optional

from sqlalchemy import BigInteger, DateTime, Index, Integer, String, text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class PlantingData(Base):
    __tablename__ = 'crop_data'
    __table_args__ = (
        Index('idx_check_sum', 'check_sum'),
        Index('idx_country_province', 'country', 'province'),
        Index('ix_crop_data_check_sum', 'check_sum'),
        Index('ix_crop_data_coordinates', 'coordinates'),
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
    coordinates: Mapped[Optional[str]] = mapped_column(String(50))
    country: Mapped[Optional[str]] = mapped_column(String(20))
    province: Mapped[Optional[str]] = mapped_column(String(20))
    lon: Mapped[Optional[str]] = mapped_column(String(10))
    lat: Mapped[Optional[str]] = mapped_column(String(10))
    variety: Mapped[Optional[str]] = mapped_column(String(20))
    season_type: Mapped[Optional[str]] = mapped_column(String(20))
    opt_date: Mapped[Optional[str]] = mapped_column(String(8))
    planting_option: Mapped[Optional[int]] = mapped_column(Integer)
    created_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime, server_default=text('CURRENT_TIMESTAMP'))
    updated_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime, server_default=text('CURRENT_TIMESTAMP'))


class ProcessedFiles(Base):
    __tablename__ = 'processed_files'

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    check_sum: Mapped[str] = mapped_column(String(100), unique=True)
    file_name: Mapped[str] = mapped_column(String(120))
    processed_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime, server_default=text('CURRENT_TIMESTAMP'))
