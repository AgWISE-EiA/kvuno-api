from dataclasses import dataclass
from typing import Optional


@dataclass
class CropDataFilters:
    coordinates: Optional[str] = None
    country: Optional[str] = None
    province: Optional[str] = None
    lon: Optional[str] = None
    lat: Optional[str] = None
    variety: Optional[str] = None
    season_type: Optional[str] = None
    opt_date: Optional[str] = None
    planting_option: Optional[int] = None
    check_sum: Optional[str] = None
