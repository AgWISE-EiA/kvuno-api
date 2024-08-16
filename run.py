"""
This script initializes and runs a Flask web application.

The script performs the following steps:
1. Loads environment variables from a `.env` file using `python-dotenv`.
2. Creates an instance of the Flask application using a factory method `create_app()`.
3. Retrieves the Flask debug mode, server host, and port settings from environment variables.
4. Runs the Flask application with the specified host, port, and debug mode.

Environment Variables:
- `FLASK_DEBUG`: If set to '1', the application will run in debug mode.
- `SERVER_HOST`: Specifies the host address on which the Flask app will run. Defaults to '0.0.0.0'.
- `SERVER_PORT`: Specifies the port on which the Flask app will run. Defaults to 5000.

Usage:
- Run this script directly to start the Flask application.

Example:
    $ python run.py
"""

import os

from dotenv import load_dotenv

from app import create_app

load_dotenv()

app = create_app()

if __name__ == '__main__':
    # Use environment variables
    debug = os.getenv('FLASK_DEBUG') == '1'
    host = os.getenv('SERVER_HOST', default='0.0.0.0')
    port = os.getenv('SERVER_PORT', default=5000)
    app.run(host=host, port=port, debug=debug)

