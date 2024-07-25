import hashlib
import os

from dotenv import load_dotenv
from loguru import logger
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app import create_app
from app.models.kvuno import ProcessedFiles

# Load environment variables from .env file
load_dotenv()


def calculate_file_checksum(file_path, algorithm='sha256'):
    """
    Calculate the checksum of a file using the specified algorithm.

    Args:
        file_path (str): Path to the file.
        algorithm (str): Hash algorithm to use (e.g., 'md5', 'sha1', 'sha256'). Default is 'sha256'.

    Returns:
        str: The checksum of the file content.
    """
    hash_func = hashlib.new(algorithm)
    logger.debug(f'Calculating checksum for {file_path} using [{algorithm}] algorithm.')
    try:
        with open(file_path, 'rb') as f:
            for chunk in iter(lambda: f.read(4096), b''):
                hash_func.update(chunk)
        return hash_func.hexdigest()
    except FileNotFoundError:
        logger.error(f"File not found: {file_path}")
    except Exception as e:
        logger.error(f"An error occurred: {e}", exc_info=True)


def load_rds_to_db(data_folder, db_session):
    # Convert to list of dictionaries
    data_records = []

    for filename in os.listdir(data_folder):

        if filename.endswith('.RDS'):
            file_path = os.path.join(data_folder, filename)
            # Check if file is already processed
            if db_session.query(ProcessedFiles).filter_by(file_name=filename).first():
                logger.info(f"File {filename} is already processed.")
                continue

            print(f"Processing file: {filename}")
            checksum = calculate_file_checksum(file_path)
            logger.debug(f"Checksum for {file_path}: {checksum}")

            # result = pyreadr.read_r(file_path)
            # data = result[None]
            # data['source'] = filename
            # for index, row in data.iterrows():
            #     record = {
            #         'XY': row['XY'],
            #         'country': row['country'],
            #         'province': row['province'],
            #         'lon': row['lon'],
            #         'lat': row['lat'],
            #         'Variety': row['Variety'],
            #         'Season_type': row['Season_type'],
            #         'Opt_date': row['Opt_date'],
            #         'Planting_Option': row['Planting_Option'],
            #         'source_file': filename
            #     }
            #     data_records.append(record)

    print(data_records)


if __name__ == '__main__':
    app = create_app()
    db_url = os.getenv('DB_URL')
    engine = create_engine(db_url)
    Session = sessionmaker(bind=engine)
    session = Session()

    # Specify the path to your RDS file
    rds_folder = os.path.join("static/" 'data')
    load_rds_to_db(rds_folder, session)
