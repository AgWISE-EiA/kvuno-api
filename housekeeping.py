import logging
import os

import pandas as pd
import pyreadr
from dotenv import load_dotenv

from app.dto.data_class import CropRecord
from app.models.kvuno import ProcessedFiles
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
    for filename in os.listdir(data_folder):

        if filename.endswith('.RDS'):
            file_path = os.path.join(data_folder, filename)
            logger.info(f"Processing file: {filename}")
            checksum = calculate_file_checksum(file_path, logger)
            logger.debug(f"Checksum for {file_path}: {checksum}")
            crop_data_records = []

            # Check if file is already processed
            if processed_files_repo.get_processed_file_by_checksum(checksum):
                logger.info(f"File {filename} is already processed.")
                continue

            result = pyreadr.read_r(file_path)
            data = result[None]
            for index, row in data.iterrows():
                logger.debug(f"Processing record {index}")

                # Convert NA values to None (which will become NULL in the database)
                record = CropRecord(
                    coordinates=row['XY'] if pd.notna(row['XY']) else None,
                    country=row['country'] if pd.notna(row['country']) else None,
                    province=row['province'] if pd.notna(row['province']) else None,
                    lon=row['lon'] if pd.notna(row['lon']) else None,
                    lat=row['lat'] if pd.notna(row['lat']) else None,
                    variety=row['Variety'] if pd.notna(row['Variety']) else None,
                    season_type=row['Season_type'] if pd.notna(row['Season_type']) else None,
                    opt_date=row['Opt_date'] if pd.notna(row['Opt_date']) else None,
                    planting_option=int(row['Planting_Option']) if pd.notna(row['Planting_Option']) else None,
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

            logger.info("Finished processing all files, now tracking checksum {checksum}")
            processed_file = ProcessedFiles(
                file_name=filename,
                check_sum=checksum
            )
            processed_files_repo.add_processed_file(processed_file=processed_file)


if __name__ == '__main__':
    rds_folder = os.path.join("static/" 'data')
    load_rds_to_db(data_folder=rds_folder, batch_size=10)
