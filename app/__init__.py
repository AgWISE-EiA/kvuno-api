import os

from dotenv import load_dotenv
from flask_openapi3 import OpenAPI, Server, Contact, License, Info
from flask_cors import CORS

from app.models.database_conn import MyDb
from app.routes.api_v1 import api_v1
from app.routes.main import register_app_routes

load_dotenv()
contact = Contact(name="Munywele Sammy", email="sammy@munywele.co.ke", url="https://munywele.co.ke")

apiLicense = License(
    name="Apache 2.0",
    identifier="Apache-2.0"
)

info = Info(title="KVuno API",
            contact=contact,
            license=apiLicense,
            termsOfService="https://agwise.cgiar.org/terms-of-service",
            version="1.0.0")

servers = [
    Server(url="http://127.0.0.1:5000"),
    Server(url=os.getenv("SERVER_URL_PROD", "https://kvuno.akilimo.org")),
]


def create_app():
    app = OpenAPI(__name__,
                  info=info,
                  servers=servers)

    CORS(app)  # Enable CORS for all routes

    # Set the SQLALCHEMY_DATABASE_URI directly in app config
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DB_URL")
    app.config['SQLALCHEMY_ECHO'] = os.getenv('DEBUG_DB') == '1'

    # Initialize the database with the Flask app
    MyDb.init_app(app)

    app.register_api(api_v1)
    app.json.sort_keys = False

    register_app_routes(app)

    return app
