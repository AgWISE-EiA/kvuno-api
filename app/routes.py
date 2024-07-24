import os

from flask import jsonify

from app import DataPreprocessor


def init_routes(app):
    @app.route('/', methods=['GET'])
    def hello_world():  # put application's code here
        return jsonify('Hello World we are here!')

    @app.route('/name/<string:name>', methods=['GET'])
    def test_string(name):
        return jsonify(f"Name to be printed is {name}")

    @app.route('/get-data', methods=['GET'])
    def get_data():
        data_folder = os.path.join(app.static_folder, 'data')

        processor = DataPreprocessor(data_folder)

        data_json = processor.get_data()
        return jsonify(data_json)
