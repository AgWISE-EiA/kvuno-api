import os
import subprocess

from dotenv import load_dotenv
from loguru import logger

# Load environment variables from .env file
load_dotenv()


def create_dummy_file(filepath):
    """Create a dummy file with placeholder content."""
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, 'w') as f:
        f.write("# This is a dummy ORM file\n")
        f.write("# Replace this content with generated ORM code\n")


def run_sqlacodegen():
    # Read environment variables
    db_url = os.getenv('DB_URL')
    outfile_path = os.getenv('OUTFILE_PATH', 'app/models/kvuno.py')

    # create dummy file
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
        logger.info("Output:\n", result.stdout)
        logger.error("Errors:\n", result.stderr)
    except subprocess.CalledProcessError as e:
        logger.error(f"An error occurred: {e}")


if __name__ == "__main__":
    run_sqlacodegen()
