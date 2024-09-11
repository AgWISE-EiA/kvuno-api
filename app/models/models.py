from geoalchemy2.types import Geometry
from sqlalchemy import BigInteger, CheckConstraint, Column, DateTime, Index, Integer, MetaData, PrimaryKeyConstraint, String, Table, Text, UniqueConstraint, text

metadata = MetaData()


t_crop_data = Table(
    'crop_data', metadata,
    Column('id', BigInteger, primary_key=True),
    Column('location', String(50), comment='Coordinates of the crop xy'),
    Column('country', String(20)),
    Column('province', String(20)),
    Column('lon', String(10)),
    Column('lat', String(10)),
    Column('variety', String(20)),
    Column('season_type', String(20)),
    Column('opt_date', String(8)),
    Column('planting_option', Integer),
    Column('check_sum', String(100), nullable=False),
    Column('created_at', DateTime, server_default=text('now()')),
    Column('updated_at', DateTime, server_default=text('now()')),
    Column('coordinates', Geometry('POINT', 4326, from_text='ST_GeomFromEWKT', name='geometry')),
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

t_geography_columns = Table(
    'geography_columns', metadata,
    Column('f_table_catalog', String),
    Column('f_table_schema', String),
    Column('f_table_name', String),
    Column('f_geography_column', String),
    Column('coord_dimension', Integer),
    Column('srid', Integer),
    Column('type', Text)
)

t_geometry_columns = Table(
    'geometry_columns', metadata,
    Column('f_table_catalog', String(256)),
    Column('f_table_schema', String),
    Column('f_table_name', String),
    Column('f_geometry_column', String),
    Column('coord_dimension', Integer),
    Column('srid', Integer),
    Column('type', String(30))
)

t_processed_files = Table(
    'processed_files', metadata,
    Column('id', BigInteger, primary_key=True),
    Column('check_sum', String(100), nullable=False),
    Column('file_name', String(120), nullable=False),
    Column('processed_at', DateTime, server_default=text('now()')),
    PrimaryKeyConstraint('id', name='processed_files_pkey'),
    UniqueConstraint('check_sum', name='processed_files_check_sum_key')
)

t_spatial_ref_sys = Table(
    'spatial_ref_sys', metadata,
    Column('srid', Integer, primary_key=True),
    Column('auth_name', String(256)),
    Column('auth_srid', Integer),
    Column('srtext', String(2048)),
    Column('proj4text', String(2048)),
    CheckConstraint('srid > 0 AND srid <= 998999', name='spatial_ref_sys_srid_check'),
    PrimaryKeyConstraint('srid', name='spatial_ref_sys_pkey')
)
