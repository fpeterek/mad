from datetime import date
from dataclasses import dataclass

from data.geo_point import GeoPoint


_cleared = ('C', 'O')


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

    @property
    def is_cleared(self) -> bool:
        global _cleared
        return self.clearance_status and self.clearance_status in _cleared
