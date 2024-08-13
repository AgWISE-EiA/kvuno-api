import logging

from sqlalchemy.orm import sessionmaker

from app.models.database_conn import MyDb
from app.models.kvuno import ProcessedFiles
from app.utils.logging import SharedLogger

shared_logger = SharedLogger(level=logging.DEBUG)


class ProcessedFilesRepo:
    def __init__(self):
        self.db_engine = MyDb()
        self.session = sessionmaker(bind=self.db_engine)
        self.db = self.session()
        self.logger = shared_logger.get_logger()

    def get_processed_files(self):
        return self.db.query(ProcessedFiles).all()

    def add_processed_file(self, processed_file):
        self.db.add(processed_file)
        self.db.commit()

    def get_processed_file_by_id(self, record_id):
        return self.db.query(ProcessedFiles).filter_by(id=record_id).first()

    def get_processed_file_by_checksum(self, checksum):
        return (self.db
                .query(ProcessedFiles, ProcessedFiles.check_sum)
                .filter_by(check_sum=checksum).first())

    def get_processed_file_by_name(self, file_name):
        return self.db.query(ProcessedFiles).filter_by(file_name=file_name).first()

    def delete_processed_file(self, processed_file):
        self.db.delete(processed_file)
        self.db.commit()

    def insert_processed_files(self, processed_files):
        self.db.add_all(processed_files)
        self.db.commit()
