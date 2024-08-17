from typing import Optional, List

from pydantic import Field, BaseModel


class Unauthorized(BaseModel):
    code: int = Field(-1, description="Status Code")
    message: str = Field("Unauthorized!", description="Exception Information")


class Coordinates(BaseModel):
    lat: str
    lon: str


class Datum(BaseModel):
    id: int
    province: str
    district: str
    aez: str
    season: str
    currentYield: str
    coordinates: Coordinates
    urea: float
    dap: float
    npk: float
    expectedYield: float
    fertilizerCost: float
    netRevenue: float


class Pagination(BaseModel):
    page: int
    per_page: int
    total_records: int
    total_pages: int
    last_page: int


class FertilizerResponse(BaseModel):
    data: List[Datum]
    pagination: Pagination


class FertilizerQuery(BaseModel):
    coordinates: Optional[str] = Field(None, description='Coordinates lat,long')
    region: Optional[str] = Field(None, description='Planting region')
    province: Optional[str] = Field(None, description='Province')
    season: Optional[str] = Field(None, description='Planting season e.g July')
    district: Optional[str] = Field(None, description='Planting district')
    limit: Optional[int] = Field(100, description='Number of records to return per page')
    page: Optional[int] = Field(1, description='Page number based on number of records in database')
    paginate: Optional[bool] = Field(True, description='Enable pagination of result or return all of it')
