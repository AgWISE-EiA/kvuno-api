from flask_openapi3 import OpenAPI, Server, Contact, License, Info

from app.routes.api_v1 import api_v1
from app.routes.app_routes import register_app_routes

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
    Server(url="https://akilimo.org:5000"),
]


def create_app():
    app = OpenAPI(__name__,
                  info=info,
                  servers=servers)

    app.register_api(api_v1)
    app.json.sort_keys = False

    register_app_routes(app)

    return app
