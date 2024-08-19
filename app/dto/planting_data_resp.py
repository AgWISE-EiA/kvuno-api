from dataclasses import dataclass
from typing import List
from typing import Optional

from pydantic import Field, BaseModel


class Unauthorized(BaseModel):
    code: int = Field(-1, description="Status Code")
    message: str = Field("Unauthorized!", description="Exception Information")


class Coordinates(BaseModel):
    lat: str
    lon: str


@dataclass
class PlantingDataRecord:
    coordinates: Optional[str]
    country: Optional[str]
    province: Optional[str]
    lon: Optional[str]
    lat: Optional[str]
    variety: Optional[str]
    season_type: Optional[str]
    opt_date: Optional[str]
    planting_option: Optional[int]
    check_sum: Optional[str]


class Pagination(BaseModel):
    total: int
    pages: int
    current_page: int
    per_page: int


class CropRecordResponse(BaseModel):
    data: List[PlantingDataRecord]
    pagination: Pagination