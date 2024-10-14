from typing import List, Optional

from pydantic import Field, BaseModel


class Unauthorized(BaseModel):
    code: int = Field(-1, description="Status Code")
    message: str = Field("Unauthorized!", description="Exception Information")


class Coordinates(BaseModel):
    lat: float
    lon: float


class CropDataRecord(BaseModel):
    id: Optional[int]  # Latitude as float
    lat: Optional[float]  # Latitude as float
    lon: Optional[float]  # Longitude as float
    country: Optional[str]
    crop_name: Optional[str]
    province: Optional[str]
    variety: Optional[str]
    season_type: Optional[str]
    opt_date: Optional[str]
    planting_option: Optional[int]
    check_sum: Optional[str]

    # class Config:
    #     orm_mode = True  # Ensures compatibility with ORM models if needed
    #


class Pagination(BaseModel):
    total: int
    pages: int
    current_page: int
    per_page: int


class CropRecordResponse(BaseModel):
    data: List[CropDataRecord]
    pagination: Pagination
