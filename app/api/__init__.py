# from flask_openapi3 import APIBlueprint
# from app.api.user import user_bp
# from app.api.crop_data import crop_data_bp
#
# # Parent API Blueprint with a common URL prefix
# api_v1_bp = APIBlueprint(
#     'api_v1',
#     __name__,
#     url_prefix='/api/v1',
#     doc_ui=True  # Enable OpenAPI UI at this level
# )
#
# # Register child blueprints
# api_v1_bp.register_blueprint(user_bp)
# api_v1_bp.register_blueprint(crop_data_bp)