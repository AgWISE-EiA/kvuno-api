from flask import Flask

from .preprocessor.data_preprocessor import DataPreprocessor
from .routes import init_routes


def create_app():
    app = Flask(__name__)

    init_routes(app)

    return app
