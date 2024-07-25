from flask import jsonify
from flask_openapi3 import APIBlueprint, Tag

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

@api_v1.get('/name/<string:name>', tags=[kvuno_tag])
def test_string(name):
    return jsonify(f"Name to be printed is {name}")


@api_v1.get("/get-data", tags=[kvuno_tag])
def get_data():
    pass
