import logging

from flask import request, jsonify
from flask_openapi3 import APIBlueprint, Tag

from app.dto.data_class import CropRecord
from app.repo.crop_data import CropDataRepo
from app.utils.logging import SharedLogger

security = [{"jwt": []}]
tag = Tag(name='AgWise', description="AgWise API")

api_v1 = APIBlueprint(
    'api_v1',
    __name__,
    url_prefix='/api/v1',
    # abp_tags=[tag],
    # abp_security=security,
    # abp_responses={"401": Unauthorized},
    # disable openapi UI
    doc_ui=True
)

kvuno_tag = Tag(name="kvuno", description="Data serving API")

shared_logger = SharedLogger(level=logging.DEBUG)
logger = shared_logger.get_logger()

crop_data_repo = CropDataRepo()


@api_v1.get("/get-data", tags=[kvuno_tag])
def get_data():
    # Extract filters and pagination parameters from request arguments
    filters = {
        'coordinates': request.args.get('coordinates'),
        'country': request.args.get('country'),
        'province': request.args.get('province'),
        'lon': request.args.get('lon'),
        'lat': request.args.get('lat'),
        'variety': request.args.get('variety'),
        'season_type': request.args.get('season_type'),
        'opt_date': request.args.get('opt_date'),
        'planting_option': request.args.get('planting_option'),
        'check_sum': request.args.get('check_sum'),
    }

    # Remove any None values from the filters dictionary
    filters = {k: v for k, v in filters.items() if v is not None}

    page = int(request.args.get('page', 1))
    per_page = int(request.args.get('per_page', 1))
    try:
        paginated_data = crop_data_repo.get_paginated_data(filters, page, per_page)

        # Convert the result to a list of dictionaries for JSON serialization
        data = [CropRecord(
            coordinates=item.coordinates,
            country=item.country,
            province=item.province,
            lon=item.lon,
            lat=item.lat,
            variety=item.variety,
            season_type=item.season_type,
            opt_date=item.opt_date,
            planting_option=item.planting_option,
            check_sum=item.check_sum
        ).__dict__ for item in paginated_data.items]

        # Format the paginated data as JSON
        response = {
            'data': data,
            'total': paginated_data.total,
            'pages': paginated_data.pages,
            'current_page': paginated_data.page,
            'per_page': paginated_data.per_page
        }

        return jsonify(response), 200

    except Exception as e:
        # Handle errors and return an appropriate response
        return jsonify({'error': str(e)}), 500


@api_v1.get("/get-data-old", tags=[kvuno_tag])
def get_data_old():
    # Retrieve query parameters
    page = int(request.args.get('page', 1))  # Default to page 1
    per_page = int(request.args.get('per_page', 10))  # Default to 10 items per page
    filter_column = request.args.get('filter_column', None)
    filter_value = request.args.get('filter_value', None)
    columns = request.args.getlist('columns')  # List of columns to return

    # Retrieve filter parameters as a dictionary
    filters = {key: value for key, value in request.args.items() if key not in ['page', 'per_page', 'columns']}

    # Validate and sanitize parameters
    if per_page <= 0:
        per_page = 10  # Default to 10 if invalid per_page
    if page <= 0:
        page = 1  # Default to page 1 if invalid page

    # Apply column filtering
    if filters:
        data = crop_data_repo.get_filtered_data(filters, page, per_page)
    else:
        data = crop_data_repo.get_all(page, per_page)

    # Apply column selection
    if columns:
        data = [{col: row.get(col) for col in columns if col in row} for row in data]

    return jsonify(data)
