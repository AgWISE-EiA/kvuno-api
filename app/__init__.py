import os

from dotenv import load_dotenv
from flask_cors import CORS
from flask_openapi3 import OpenAPI, Server, Contact, License, Info

from app.models.database_conn import MyDb
from app.routes.api_v1 import api_v1
from app.routes.main import register_app_routes
from . import config

# Load environment variables from .env file
load_dotenv()

# API contact information
contact = Contact(
    name="Munywele Sammy",
    email="sammy@munywele.co.ke",
    url="https://munywele.co.ke"
)

# API license information
api_license = License(
    name="Apache 2.0",
    identifier="Apache-2.0"
)

# API information
info = Info(
    title=config.APP_NAME,
    version=config.APP_VERSION,
    contact=contact,
    license=api_license,
    termsOfService="https://agwise.cgiar.org/terms-of-service"
)

# API servers
servers = [
    Server(url="http://127.0.0.1:5000"),
    Server(url=os.getenv("SERVER_URL_PROD", "https://kvuno.akilimo.org")),
]


def init_db(app):
    """Initialize the database with the Flask app."""
    MyDb.init_app(app)


def register_apis(app: OpenAPI):
    """Register all API Blueprints with the Flask app."""
    from app.api.user import api as user_api
    from app.api.planting_data import api as planting_data_api

    app.register_api(user_api)
    app.register_api(planting_data_api)


def create_app():
    """Create and configure the Flask app."""
    app = OpenAPI(
        __name__,
        servers=servers,
        info=info,
        security_schemes={
            "basic": {"type": "http", "scheme": "basic"},
            "jwt": {"type": "http", "scheme": "bearer", "bearerFormat": "JWT"}
        }
    )

    # Enable Cross-Origin Resource Sharing (CORS)
    CORS(app)

    # Configure the database URI
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DB_URL")
    app.config['SQLALCHEMY_ECHO'] = os.getenv('DEBUG_DB') == '1'

    # Initialize the database
    init_db(app)

    # Register APIs and other routes
    register_apis(app)
    register_app_routes(app)

    return app
