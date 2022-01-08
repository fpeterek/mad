from datetime import date
from dataclasses import dataclass

from data.geo_point import GeoPoint


@dataclass
class CrimeRecord:
    key: int
    council_district: int | None
    highest_offense: str
    crime_type: str
    report_date: date
    location: str | None
    coordinates: GeoPoint | None
    clearance_status: str | None
    clearance_date: date | None
    go_district: str
    go_zip_code: int | None
    go_census_tract: str | None
    clearance_time: int | None
