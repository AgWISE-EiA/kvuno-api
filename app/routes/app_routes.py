from flask import redirect


def register_app_routes(app):
    """
    Register routes for the Flask application.

    Args:
        app (Flask): The Flask application instance.
    """

    @app.route('/')
    def index():
        """
        Route for the root URL.

        Returns:
            Response: Redirect to /openapi/rapidoc.
        """
        return redirect('/openapi/rapidoc')
