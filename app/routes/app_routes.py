from flask import jsonify


def register_app_routes(app):
    """
    Register routes for the Flask application.

    Args:
        app (Flask): The Flask application instance.
    """

    @app.route('/')
    def app_test():
        """
        Route for the root URL.

        Returns:
            Response: JSON response with a test message.
        """
        return jsonify('This is a route defined with @app')

    @app.route('/app-name/<string:name>')
    def app_name(name):
        """
        Route for the app name URL.

        Args:
            name (str): The name parameter from the URL.

        Returns:
            Response: JSON response with the app route name.
        """
        return jsonify(f"App route name: {name}")
