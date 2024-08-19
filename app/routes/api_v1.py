import logging

from flask import request, jsonify
from flask_openapi3 import APIBlueprint, Tag

from app.dto.api_responses import PlantingDataRecord, CropRecordResponse, Unauthorized
from app.dto.data_filters import PlantingDataFilter
from app.repo.planting_data import PlantingDataRepo
from app.utils.logging import SharedLogger

security = [{"jwt": []}]
tag = Tag(name='AgWise', description="AgWise API")

api_v1 = APIBlueprint(
    'api_v1',
    __name__,
    url_prefix='/api/v1',
    # abp_tags=[tag],
    # abp_security=security,
    # disable openapi UI
    doc_ui=True
)

kvuno_tag = Tag(name="kvuno", description="Data serving API")

shared_logger = SharedLogger(level=logging.DEBUG)
logger = shared_logger.get_logger()

crop_data_repo = PlantingDataRepo()


@api_v1.get("/crop-data",
            tags=[kvuno_tag],
            responses={200: CropRecordResponse, 401: Unauthorized}
            )
def get_data(query: PlantingDataFilter):
    page = int(request.args.get('page', default=1, type=int))
    per_page = int(request.args.get('per_page', default=50, type=int))

    try:
        paginated_data = crop_data_repo.get_paginated_data(query, page, per_page)

        # Convert the result to a list of dictionaries for JSON serialization
        data = [PlantingDataRecord(
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
