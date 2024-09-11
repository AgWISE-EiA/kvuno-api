import os
import subprocess

from dotenv import load_dotenv
from loguru import logger
from sqlalchemy import create_engine, MetaData

# Load environment variables from .env file
load_dotenv()


def create_dummy_file(filepath):
    """
    Create a dummy file with placeholder content.

    Args:
        filepath (str): The path to the file to be created.
    """
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, 'w', encoding='UTF-8') as f:
        f.write("# This is a dummy ORM file\n")
        f.write("# Replace this content with generated ORM code\n")


def get_tables_in_schema():
    """
    Retrieve the list of tables in the database schema.

    Reads the database URL from environment variables, connects to the database,
    and returns the list of table names in the current schema.

    Returns:
        list: A list of table names in the schema.
    """
    db_url = os.getenv('DB_URL')

    if not db_url:
        raise ValueError("DB_URL environment variable is not set")

    # Create the database engine
    engine = create_engine(db_url)

    # Reflect the database schema
    metadata = MetaData()
    metadata.reflect(bind=engine)

    # Get the list of tables
    tables = list(metadata.tables.keys())

    # Log the table names
    logger.info(f"Tables in schema: {tables}")

    return tables


def run_sqlacodegen():
    """
    Run the sqlacodegen tool to generate model classes from the database schema.

    Reads environment variables for database URL and output file path,
    executes the `sqlacodegen` command, and handles any errors that occur.

    Environment Variables:
        - DB_URL: The database connection URL.
        - OUTFILE_PATH: The path where the generated model file will be saved (default: 'app/models/kvuno.py').
        - EXCLUDED_TABLES: Comma-separated names of tables to exclude from generation.

    Raises:
        RuntimeError: If the sqlacodegen command fails.
    """
    # Read environment variables
    db_url = os.getenv('DB_URL')
    outfile_path = os.getenv('OUTFILE_PATH', 'app/models/kvuno.py')
    excluded_tables = os.getenv('EXCLUDED_TABLES', 'spatial_ref_sys').split(',')

    # Create dummy file
    create_dummy_file(outfile_path)

    try:
        # Get all tables from the database

        all_tables = get_tables_in_schema()

        # Filter out excluded tables
        included_tables = [table for table in all_tables if table not in excluded_tables]

        if not included_tables:
            logger.warning("No tables left to generate models after exclusions.")
            exit(100)

        # Construct the command to generate models for the included tables
        command = [
            'sqlacodegen',
            db_url,
            '--outfile',
            outfile_path,
            '--tables',
            ','.join(included_tables)
        ]

        result = subprocess.run(command, check=True, capture_output=True, text=True)
        logger.info("Output:\n" + result.stdout)
        logger.error("Errors:\n" + result.stderr)
    except subprocess.CalledProcessError as e:
        logger.error(f"An error occurred: {e}")
        raise RuntimeError(f"sqlacodegen failed: {e}") from e


if __name__ == "__main__":
    run_sqlacodegen()
