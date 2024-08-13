import logging
import os

import pyreadr
from dotenv import load_dotenv

from app.dto.data_class import CropRecord
from app.repo.crop_data import CropDataRepo
from app.repo.processed_files import ProcessedFilesRepo
from app.utils import calculate_file_checksum
from app.utils.logging import SharedLogger

# Load environment variables from .env file
load_dotenv()
shared_logger = SharedLogger(level=logging.DEBUG)
logger = shared_logger.get_logger()

processed_files_repo = ProcessedFilesRepo()
crop_data_repo = CropDataRepo()


def load_rds_to_db(data_folder, batch_size: int = 1000):
    # Convert to list of dictionaries
    crop_data_records = []

    for filename in os.listdir(data_folder):

        if filename.endswith('.RDS'):
            file_path = os.path.join(data_folder, filename)
            logger.info(f"Processing file: {filename}")
            checksum = calculate_file_checksum(file_path, logger)
            logger.debug(f"Checksum for {file_path}: {checksum}")

            # Check if file is already processed
            if processed_files_repo.get_processed_file_by_checksum(checksum):
                logger.info(f"File {filename} is already processed.")
                continue

            result = pyreadr.read_r(file_path)
            data = result[None]
            for index, row in data.iterrows():
                logger.info(f"Processing record {index}")
                record = CropRecord(
                    coordinates=row['XY'],
                    country=row['country'],
                    province=row['province'],
                    lon=row['lon'],
                    lat=row['lat'],
                    variety=row['Variety'],
                    season_type=row['Season_type'],
                    opt_date=row['Opt_date'],
                    planting_option=row['Planting_Option'],
                    check_sum=checksum
                )

                crop_data_records.append(record)
                if len(crop_data_records) >= batch_size:
                    crop_data_repo.batch_insert(crop_data_records)
                    crop_data_records.clear()  # clear the batch

    # Insert remaining records
    if crop_data_records:
        crop_data_repo.batch_insert(crop_data_records)
        crop_data_records.clear()

    logger.info("Finished processing all files")


if __name__ == '__main__':
    rds_folder = os.path.join("static/" 'data')
    load_rds_to_db(data_folder=rds_folder, batch_size=10)
