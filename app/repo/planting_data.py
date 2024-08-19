import logging
from typing import Optional, List, Type

from flask_sqlalchemy.pagination import QueryPagination
from sqlalchemy.orm import Query

from app.dto.planting_data_resp import PlantingDataRecord
from app.dto.data_filters import PlantingDataFilter
from app.models.database_conn import MyDb
from app.models.kvuno import PlantingData
from app.utils.logging import SharedLogger

shared_logger = SharedLogger(level=logging.DEBUG)


class PlantingDataRepo:
    def __init__(self):
        self.logger = shared_logger.get_logger()

    def _get_session(self):
        # Ensure that `MyDb` has been initialized with a Flask app
        self.db = MyDb.get_db()
        return self.db.session

    def add(self, planting_data: PlantingData) -> PlantingData:
        session = self._get_session()
        try:
            session.add(planting_data)
            session.commit()
            session.refresh(planting_data)
            self.logger.info(f"Added PlantingData with ID: {planting_data.id}")
            return planting_data
        except Exception as e:
            session.rollback()
            self.logger.error(f"Failed to add PlantingData: {e}")
            raise

    def get_by_id(self, planting_id: int) -> Optional[PlantingData]:
        session = self._get_session()
        try:
            planting_data = session.query(PlantingData).filter_by(id=planting_id).first()
            self.logger.info(f"Retrieved PlantingData with ID: {planting_id}")
            return planting_data
        except Exception as e:
            self.logger.error(f"Failed to retrieve PlantingData with ID {planting_id}: {e}")
            raise

    def get_all(self, page, per_page) -> list[Type[PlantingData]]:
        session = self._get_session()
        offset = (page - 1) * per_page
        try:
            planting_data_list = (session.query(PlantingData)
                                  .offset(offset)
                                  .limit(per_page)
                                  .all())

            self.logger.info("Retrieved all PlantingData records")
            return planting_data_list
        except Exception as e:
            self.logger.error(f"Failed to retrieve all PlantingData records: {e}")
            raise

    def get_filtered_data(self, filters: PlantingDataFilter) -> Query:

        session = self._get_session()

        query = session.query(PlantingData)

        if filters.coordinates:
            query = query.filter(PlantingData.coordinates == filters.coordinates)
        if filters.country:
            query = query.filter(PlantingData.country == filters.country)
        if filters.province:
            # Perform partial search for province
            query = query.filter(PlantingData.province.ilike(f"%{filters.province}%"))
        if filters.lon:
            query = query.filter(PlantingData.lon == filters.lon)
        if filters.lat:
            query = query.filter(PlantingData.lat == filters.lat)
        if filters.variety:
            query = query.filter(PlantingData.variety == filters.variety)
        if filters.season_type:
            query = query.filter(PlantingData.season_type == filters.season_type)
        if filters.opt_date:
            query = query.filter(PlantingData.opt_date == filters.opt_date)
        if filters.planting_option is not None:
            query = query.filter(PlantingData.planting_option == filters.planting_option)

        return query

    def get_paginated_data(self, filters: PlantingDataFilter, page: int, per_page: int) -> QueryPagination:
        query = self.get_filtered_data(filters)

        return query.paginate(page=page, per_page=per_page, error_out=False)

    def update(self, planting_data: PlantingData) -> PlantingData:
        session = self._get_session()
        try:
            session.commit()
            session.refresh(planting_data)
            self.logger.info(f"Updated PlantingData with ID: {planting_data.id}")
            return planting_data
        except Exception as e:
            session.rollback()
            self.logger.error(f"Failed to update PlantingData with ID {planting_data.id}: {e}")
            raise

    def delete(self, planting_data: PlantingData) -> None:
        session = self._get_session()
        try:
            session.delete(planting_data)
            session.commit()
            self.logger.info(f"Deleted PlantingData with ID: {planting_data.id}")
        except Exception as e:
            session.rollback()
            self.logger.error(f"Failed to delete PlantingData with ID {planting_data.id}: {e}")
            raise

    def find_by_checksum(self, check_sum: str) -> Optional[PlantingData]:
        session = self._get_session()
        try:
            planting_data = (session.query(PlantingData)
                             .filter_by(check_sum=check_sum).first())
            self.logger.info(f"Retrieved PlantingData with checksum: {check_sum}")
            return planting_data
        except Exception as e:
            self.logger.error(f"Failed to find PlantingData with checksum {check_sum}: {e}")
            raise

    def batch_insert(self, planting_data: List[PlantingDataRecord]) -> None:
        session = self._get_session()
        try:
            mappings = [record.__dict__ for record in planting_data]
            session.bulk_insert_mappings(PlantingData, mappings)
            session.commit()
            self.logger.info(f"Batch inserted {len(planting_data)} PlantingData records")
        except Exception as e:
            session.rollback()
            self.logger.error(f"Failed to batch insert PlantingData records: {e}")
            raise
