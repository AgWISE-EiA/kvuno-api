"""
This script initializes and runs a Flask web application.

The script performs the following steps:
1. Loads environment variables from a `.env` file using `python-dotenv`.
2. Creates an instance of the Flask application using a factory method `create_app()`.
3. Runs the Flask application in debug mode if specified in the environment variables.

Environment Variables:
- `FLASK_DEBUG`: If set to '1', the application will run in debug mode.

Usage:
- Run this script directly to start the Flask application.
"""

import os
from dotenv import load_dotenv
from app import create_app

load_dotenv()

app = create_app()

if __name__ == '__main__':
    # Use environment variables
    debug = os.getenv('FLASK_DEBUG') == '1'
    app.run(debug=debug)
