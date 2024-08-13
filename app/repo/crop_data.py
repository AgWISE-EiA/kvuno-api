import logging
from typing import Optional, List, Type

from sqlalchemy.orm import sessionmaker

from app.dto.data_class import CropRecord
from app.models.database_conn import MyDb
from app.models.kvuno import CropData
from app.utils.logging import SharedLogger

shared_logger = SharedLogger(level=logging.DEBUG)


class CropDataRepo:
    def __init__(self):
        self.db_engine = MyDb()
        self.session = sessionmaker(bind=self.db_engine)
        self.db = self.session()
        self.logger = shared_logger.get_logger()

    def add(self, crop_data: CropData) -> CropData:
        self.db.add(crop_data)
        self.db.commit()
        self.db.refresh(crop_data)
        self.logger.info(f"Added CropData with ID: {crop_data.id}")
        return crop_data

    def get_by_id(self, crop_id: int) -> Optional[CropData]:
        crop_data = self.db.query(CropData).filter_by(id=crop_id).first()
        self.logger.info(f"Retrieved CropData with ID: {crop_id}")
        return crop_data

    def get_all(self) -> list[Type[CropData]]:
        crop_data_list = self.db.query(CropData).all()
        self.logger.info("Retrieved all CropData records")
        return crop_data_list

    def update(self, crop_data: CropData) -> CropData:
        self.db.commit()
        self.db.refresh(crop_data)
        self.logger.info(f"Updated CropData with ID: {crop_data.id}")
        return crop_data

    def delete(self, crop_data: CropData) -> None:
        self.db.delete(crop_data)
        self.db.commit()
        self.logger.info(f"Deleted CropData with ID: {crop_data.id}")

    def find_by_checksum(self, check_sum: str) -> Optional[CropData]:
        crop_data = (self.db
                     .query(CropData, CropData.check_sum)
                     .filter_by(check_sum=check_sum).first())

        self.logger.info(f"Retrieved CropData with checksum: {check_sum}")
        return crop_data

    def batch_insert(self, crop_records: List[CropRecord]) -> None:
        try:
            mappings = [record.__dict__ for record in crop_records]
            self.db.bulk_insert_mappings(CropData, mappings)
            self.db.commit()
            self.logger.info(f"Batch inserted {len(crop_records)} CropData records")
        except Exception as e:
            self.db.rollback()
            self.logger.error(f"Failed to batch insert CropData records: {e}")
            raise
