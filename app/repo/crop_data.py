import logging
from typing import Optional, List, Type, Dict

from flask_sqlalchemy.pagination import QueryPagination
from sqlalchemy import and_
from sqlalchemy.orm import Query

from app.dto.data_class import CropRecord
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
            self.logger.info(f"Added CropData with ID: {crop_data.id}")
            return crop_data
        except Exception as e:
            session.rollback()
            self.logger.error(f"Failed to add CropData: {e}")
            raise

    def get_by_id(self, crop_id: int) -> Optional[CropData]:
        session = self._get_session()
        try:
            crop_data = session.query(CropData).filter_by(id=crop_id).first()
            self.logger.info(f"Retrieved CropData with ID: {crop_id}")
            return crop_data
        except Exception as e:
            self.logger.error(f"Failed to retrieve CropData with ID {crop_id}: {e}")
            raise

    def get_all(self, page, per_page) -> list[Type[CropData]]:
        session = self._get_session()
        offset = (page - 1) * per_page
        try:
            crop_data_list = (session.query(CropData)
                              .offset(offset)
                              .limit(per_page)
                              .all())

            self.logger.info("Retrieved all CropData records")
            return crop_data_list
        except Exception as e:
            self.logger.error(f"Failed to retrieve all CropData records: {e}")
            raise

    def get_filtered_data(self, filters: dict) -> Query:

        session = self._get_session()

        query = session.query(CropData)

        if 'coordinates' in filters:
            query = query.filter(CropData.coordinates == filters['coordinates'])
        if 'country' in filters:
            query = query.filter(CropData.country == filters['country'])
        if 'province' in filters:
            query = query.filter(CropData.province == filters['province'])
        if 'lon' in filters:
            query = query.filter(CropData.lon == filters['lon'])
        if 'lat' in filters:
            query = query.filter(CropData.lat == filters['lat'])
        if 'variety' in filters:
            query = query.filter(CropData.variety == filters['variety'])
        if 'season_type' in filters:
            query = query.filter(CropData.season_type == filters['season_type'])
        if 'opt_date' in filters:
            query = query.filter(CropData.opt_date == filters['opt_date'])
        if 'planting_option' in filters:
            query = query.filter(CropData.planting_option == filters['planting_option'])
        if 'check_sum' in filters:
            query = query.filter(CropData.check_sum == filters['check_sum'])

        return query

    def get_paginated_data(self, filters: dict, page: int, per_page: int) -> QueryPagination:
        query = self.get_filtered_data(filters)

        return query.paginate(page=page, per_page=per_page, error_out=False)

    # def get_paginated_data(self, filters: dict, page: int, per_page: int):
    #     query = self.get_filtered_data(filters)
    #     total_items = query.count()  # Get total number of items
    #     paginated_data = query.offset((page - 1) * per_page).limit(per_page).all()
    #     total_pages = (total_items + per_page - 1) // per_page  # Calculate total pages
    #     return paginated_data, total_items, total_pages

    def get_filtered_data_old(self, filters: Dict[str, str], page: int, per_page: int) -> list:

        session = self._get_session()

        offset = (page - 1) * per_page

        # Build filter conditions
        filter_conditions = [getattr(CropData, column) == value for column, value in filters.items() if
                             hasattr(CropData, column)]

        # Apply filter conditions
        if filter_conditions:
            query = session.query(CropData).filter(and_(*filter_conditions))
        else:
            query = session.query(CropData)

        return query.offset(offset).limit(per_page).all()

    def update(self, crop_data: CropData) -> CropData:
        session = self._get_session()
        try:
            session.commit()
            session.refresh(crop_data)
            self.logger.info(f"Updated CropData with ID: {crop_data.id}")
            return crop_data
        except Exception as e:
            session.rollback()
            self.logger.error(f"Failed to update CropData with ID {crop_data.id}: {e}")
            raise

    def delete(self, crop_data: CropData) -> None:
        session = self._get_session()
        try:
            session.delete(crop_data)
            session.commit()
            self.logger.info(f"Deleted CropData with ID: {crop_data.id}")
        except Exception as e:
            session.rollback()
            self.logger.error(f"Failed to delete CropData with ID {crop_data.id}: {e}")
            raise

    def find_by_checksum(self, check_sum: str) -> Optional[CropData]:
        session = self._get_session()
        try:
            crop_data = (session.query(CropData)
                         .filter_by(check_sum=check_sum).first())
            self.logger.info(f"Retrieved CropData with checksum: {check_sum}")
            return crop_data
        except Exception as e:
            self.logger.error(f"Failed to find CropData with checksum {check_sum}: {e}")
            raise

    def batch_insert(self, crop_records: List[CropRecord]) -> None:
        session = self._get_session()
        try:
            mappings = [record.__dict__ for record in crop_records]
            session.bulk_insert_mappings(CropData, mappings)
            session.commit()
            self.logger.info(f"Batch inserted {len(crop_records)} CropData records")
        except Exception as e:
            session.rollback()
            self.logger.error(f"Failed to batch insert CropData records: {e}")
            raise
