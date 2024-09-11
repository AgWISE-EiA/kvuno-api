import logging
from typing import Optional, List, Type

from app.dto.crop_data_resp import CropDataRecord
from flask_sqlalchemy.pagination import QueryPagination
from sqlalchemy.orm import Query

from app.dto.data_filters import PlantingDataFilter
from app.models.database_conn import MyDb
from app.models.kvuno import CropData
from app.utils.logging import SharedLogger

shared_logger = SharedLogger(level=logging.DEBUG)


class CropDataRepo:
    def __init__(self):
        self.logger = shared_logger.get_logger()

    def _get_session(self):
        # Ensure that `MyDb` has been initialized with a Flask app
        self.db = MyDb.get_db()
        return self.db.session

    def add(self, crop_data: CropData) -> CropData:
        session = self._get_session()
        try:
            session.add(crop_data)
            session.commit()
            session.refresh(crop_data)
            self.logger.info(f"Added PlantingData with ID: {crop_data.id}")
            return crop_data
        except Exception as e:
            session.rollback()
            self.logger.error(f"Failed to add PlantingData: {e}")
            raise

    def get_by_id(self, planting_id: int) -> Optional[CropData]:
        session = self._get_session()
        try:
            crop_data = session.query(CropData).filter_by(id=planting_id).first()
            self.logger.info(f"Retrieved PlantingData with ID: {planting_id}")
            return crop_data
        except Exception as e:
            self.logger.error(f"Failed to retrieve PlantingData with ID {planting_id}: {e}")
            raise

    def get_all(self, page, per_page) -> list[Type[CropData]]:
        session = self._get_session()
        offset = (page - 1) * per_page
        try:
            crop_data_list = (session.query(CropData)
                              .offset(offset)
                              .limit(per_page)
                              .all())

            self.logger.info("Retrieved all PlantingData records")
            return crop_data_list
        except Exception as e:
            self.logger.error(f"Failed to retrieve all PlantingData records: {e}")
            raise

    def get_filtered_data(self, filters: PlantingDataFilter) -> Query:

        session = self._get_session()

        query = session.query(CropData)

        if filters.coordinates:
            query = query.filter(CropData.coordinates == filters.coordinates)
        if filters.country:
            query = query.filter(CropData.country == filters.country)
        if filters.province:
            # Perform partial search for province
            query = query.filter(CropData.province.ilike(f"%{filters.province}%"))
        if filters.lon:
            query = query.filter(CropData.lon == filters.lon)
        if filters.lat:
            query = query.filter(CropData.lat == filters.lat)
        if filters.variety:
            query = query.filter(CropData.variety == filters.variety)
        if filters.season_type:
            query = query.filter(CropData.season_type == filters.season_type)
        if filters.opt_date:
            query = query.filter(CropData.opt_date == filters.opt_date)
        if filters.planting_option is not None:
            query = query.filter(CropData.planting_option == filters.planting_option)

        return query

    def get_paginated_data(self, filters: PlantingDataFilter, page: int, per_page: int) -> QueryPagination:
        query = self.get_filtered_data(filters)

        return query.paginate(page=page, per_page=per_page, error_out=False)

    def update(self, crop_data: CropData) -> CropData:
        session = self._get_session()
        try:
            session.commit()
            session.refresh(crop_data)
            self.logger.info(f"Updated PlantingData with ID: {crop_data.id}")
            return crop_data
        except Exception as e:
            session.rollback()
            self.logger.error(f"Failed to update PlantingData with ID {crop_data.id}: {e}")
            raise

    def delete(self, crop_data: CropData) -> None:
        session = self._get_session()
        try:
            session.delete(crop_data)
            session.commit()
            self.logger.info(f"Deleted PlantingData with ID: {crop_data.id}")
        except Exception as e:
            session.rollback()
            self.logger.error(f"Failed to delete PlantingData with ID {crop_data.id}: {e}")
            raise

    def find_by_checksum(self, check_sum: str) -> Optional[CropData]:
        session = self._get_session()
        try:
            crop_data = (session.query(CropData)
                         .filter_by(check_sum=check_sum).first())
            self.logger.info(f"Retrieved PlantingData with checksum: {check_sum}")
            return crop_data
        except Exception as e:
            self.logger.error(f"Failed to find PlantingData with checksum {check_sum}: {e}")
            raise

    def batch_insert(self, crop_data: List[CropDataRecord]) -> None:
        session = self._get_session()
        try:
            mappings = [record.__dict__ for record in crop_data]
            session.bulk_insert_mappings(CropData, mappings)
            session.commit()
            self.logger.info(f"Batch inserted {len(crop_data)} PlantingData records")
        except Exception as e:
            session.rollback()
            self.logger.error(f"Failed to batch insert PlantingData records: {e}")
            raise
