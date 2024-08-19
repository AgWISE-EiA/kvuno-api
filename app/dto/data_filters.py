from dataclasses import dataclass
from typing import Optional

from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from dataclasses import dataclass, field as dataclass_field


@dataclass
class CropDataFiltersBase:
    coordinates: Optional[str] = Field(None, description='Coordinates in lon,lat format')
    country: Optional[str] = Field(None, description='Country where the crop is located')
    province: Optional[str] = Field(None, description='Province where the crop is located')
    lon: Optional[str] = Field(None, description='Longitude coordinate')
    lat: Optional[str] = Field(None, description='Latitude coordinate')
    variety: Optional[str] = Field(None, description='Crop variety')
    season_type: Optional[str] = Field(None, description='Type of season, e.g., Average, High')
    opt_date: Optional[str] = Field(None, description='Optional date in YYYY-MM-DD format')
    planting_option: Optional[int] = Field(None, description='Option for planting, typically an integer')


class CropDataFilters(BaseModel, CropDataFiltersBase):
    model_config = ConfigDict(
        use_enum_values=True,
        str_strip_whitespace=True
    )
