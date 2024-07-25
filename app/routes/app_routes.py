from flask import jsonify


def register_app_routes(app):
    @app.route('/')
    def app_test():
        return jsonify('This is a route defined with @app')

    @app.route('/app-name/<string:name>')
    def app_name(name):
        return jsonify(f"App route name: {name}")
