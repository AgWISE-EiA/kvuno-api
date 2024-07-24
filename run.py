import os

from dotenv import load_dotenv

from app import create_app

load_dotenv()

app = create_app()

if __name__ == '__main__':
    # Use environment variables
    debug = os.getenv('FLASK_DEBUG') == '1'
    app.run(debug=debug)
