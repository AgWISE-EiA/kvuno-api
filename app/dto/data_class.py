import decimal
from dataclasses import dataclass
from typing import Optional


@dataclass
class CropRecord:
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
