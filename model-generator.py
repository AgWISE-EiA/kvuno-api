"""
model-generator.py

This module generates model files based on the provided database schema or configuration.

It includes functionalities for:
- Loading environment variables from a `.env` file.
- Creating a dummy file with placeholder content if necessary.
- Running the `sqlacodegen` command to generate model classes from the database schema.
- Handling subprocess errors and logging output and errors.

Usage:
    Run this module to generate models from specified database schemas using the `sqlacodegen` tool.
    Ensure that the environment variables `DB_URL` and `OUTFILE_PATH` are set correctly.
"""

import os
import subprocess

from dotenv import load_dotenv
from loguru import logger

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


def run_sqlacodegen():
    """
    Run the sqlacodegen tool to generate model classes from the database schema.

    Reads environment variables for database URL and output file path,
    executes the `sqlacodegen` command, and handles any errors that occur.

    Environment Variables:
        - DB_URL: The database connection URL.
        - OUTFILE_PATH: The path where the generated model file will be saved (default: 'app/models/kvuno.py').

    Raises:
        RuntimeError: If the sqlacodegen command fails.
    """
    # Read environment variables
    db_url = os.getenv('DB_URL')
    outfile_path = os.getenv('OUTFILE_PATH', 'app/models/kvuno.py')

    # Create dummy file
    create_dummy_file(outfile_path)

    # Construct the command
    command = [
        'sqlacodegen',
        db_url,
        '--outfile',
        outfile_path
    ]

    try:
        result = subprocess.run(command, check=True, capture_output=True, text=True)
        logger.info("Output:\n" + result.stdout)
        logger.error("Errors:\n" + result.stderr)
    except subprocess.CalledProcessError as e:
        logger.error(f"An error occurred: {e}")
        raise RuntimeError(f"sqlacodegen failed: {e}") from e


if __name__ == "__main__":
    run_sqlacodegen()
