from datetime import date
from typing import Optional

from geo_point import GeoPoint


class CrimeRecord:
    def __init__(self, key: int, council_district: Optional[int], highest_offense: str, crime_type: str,
                 report_date: date, location: Optional[str], coordinates: Optional[GeoPoint],
                 clearance_status: Optional[str], clearance_date: Optional[date], go_district: str,
                 go_zip_code: Optional[int], go_census_tract: Optional[str], clearance_time: Optional[int]):
        self.key = key
        self.council_district = council_district
        self.highest_offense = highest_offense
        self.crime_type = crime_type
        self.report_date = report_date
        self.location = location
        self.coordinates = coordinates
        self.clearance_status = clearance_status
        self.clearance_date = clearance_date
        self.go_district = go_district
        self.go_zip_code = go_zip_code
        self.go_census_tract = go_census_tract
        self.clearance_time = clearance_time
