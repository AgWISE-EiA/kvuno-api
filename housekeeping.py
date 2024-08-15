"""
Housekeeping script that processes RDS files and inserts data into the database
"""
import concurrent.futures
import logging
import os
import time

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


def process_file(file_path: str, batch_size: int = 1000, chunk_size: int = 10000):
    """
    Processes a single file by reading its contents in chunks, converting data to `CropRecord` instances,
    and inserting records into the database. The file is only processed if its checksum is not
    already recorded in the processed_files repository.

    Args:
        file_path (str): The path to the file to be processed.
        batch_size (int): The number of records to batch insert into the database. Defaults to 1000.
        chunk_size (int): The number of rows to read at a time from the RDS file. Defaults to 10000.

    Raises:
        FileNotFoundError: If the specified file is not found.
    """

    start_time = time.time()  # Start timing
    file_name = os.path.basename(file_path)  # Extract the filename without path

    try:
        checksum = calculate_file_checksum(file_path, logger)

        if processed_files_repo.get_processed_file_by_checksum(checksum):
            logger.warning(f"File {file_name} is already processed. Checksum: {checksum}")
            return  # Skip processing if file is already processed

        logger.info(f"Processing file {file_name} in chunks of size {chunk_size}")

        # Initialize batch processing
        crop_data_records = []

        result = pyreadr.read_r(file_path)
        data = result[None]  # Assuming this returns a DataFrame or equivalent
        num_rows = len(data)

        # Process the file in chunks
        for start in range(0, num_rows, chunk_size):
            end = min(start + chunk_size, num_rows)
            chunk = data.iloc[start:end]

            logger.debug(f"Processing chunk from rows {start} to {end} of {file_name}")

            for index, row in chunk.iterrows():
                logger.debug(f"Processing row {index} from {file_name}")
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
                    logger.info(f"Processed batch of {len(crop_data_records)} records from {file_name}")
                    crop_data_records.clear()  # Clear the batch

        # Insert remaining records
        if crop_data_records:
            logger.info(f"Inserting final batch of {len(crop_data_records)} records")
            crop_data_repo.batch_insert(crop_data_records)
            crop_data_records.clear()

        processed_file = ProcessedFiles(
            file_name=file_name,
            check_sum=checksum
        )
        processed_files_repo.add_processed_file(processed_file=processed_file)
        logger.info(f"File {file_name} processed and recorded")

    except FileNotFoundError as e:
        logger.error(f"Failed to process file {file_name}: {e}")
    except Exception as e:
        logger.error(f"Unexpected error processing file {file_name}: {e}")
    finally:
        elapsed_time = time.time() - start_time
        logger.info(f"Processing file {file_name} took {elapsed_time:.2f} seconds")


def load_rds_to_db(data_folder: str, batch_size: int = 1000, chunk_size: int = 10000):
    """
    Loads and processes all RDS files from a specified directory by submitting them for processing
    using a process pool executor. Each file is processed in a separate process.

    Args:
        data_folder (str): The directory containing the RDS files to be processed.
        batch_size (int): The number of records to batch insert into the database. Defaults to 1000.
        chunk_size (int): The number of rows to read at a time from each RDS file. Defaults to 10000.
    """
    file_paths = [os.path.join(data_folder, f) for f in os.listdir(data_folder) if f.endswith('.RDS')]

    global_start_time = time.time()  # Start timing
    logger.info(f"Starting to process {len(file_paths)} files from {data_folder}")

    with concurrent.futures.ThreadPoolExecutor() as executor:
        executor.map(lambda file_path: process_file(file_path, batch_size, chunk_size), file_paths)

    global_elapsed_time = time.time() - global_start_time
    logger.info(f"Processing all files  took {global_elapsed_time:.2f} seconds")


if __name__ == '__main__':
    rds_folder = os.path.join("static/", 'data')
    load_rds_to_db(data_folder=rds_folder, batch_size=1000, chunk_size=10000)
