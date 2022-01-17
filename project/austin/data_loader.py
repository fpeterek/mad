from datetime import datetime
import csv

from data.crime_record import CrimeRecord
from data.geo_point import GeoPoint


class DataLoader:

    @staticmethod
    def parse_line(line: list) -> CrimeRecord:
        split = line[:]
        key = int(split[0])
        district = int(split[1]) if split[1] else None
        highest_offense = split[2]
        crime_type = split[3]
        report_date = datetime.strptime(split[4], '%d-%b-%y').date()
        location = split[5] if split[5] and split[5] != '""' else None
        coordinates = None
        if split[6] and split[7]:
            coordinates = GeoPoint(lat=float(split[6]), lon=float(split[7]))
        clearance_status = split[8] if split[8] else None
        clearance_date = None if not split[9] else datetime.strptime(split[9], '%d-%b-%y').date()
        go_district = split[10]
        go_zip_code = int(split[11]) if split[11] else None
        go_census_tract = split[12] if split[12] else None
        clearance_time = (clearance_date - report_date).days if clearance_date else None

        return CrimeRecord(key=key, council_district=district, highest_offense=highest_offense, crime_type=crime_type,
                           report_date=report_date, location=location, coordinates=coordinates,
                           clearance_status=clearance_status, clearance_date=clearance_date, go_district=go_district,
                           go_zip_code=go_zip_code, go_census_tract=go_census_tract, clearance_time=clearance_time)

    @staticmethod
    def load_data(filename: str) -> list[CrimeRecord]:
        with open(filename, newline='') as file:
            reader = csv.reader(file, delimiter=',', quotechar='"')
            filtered = filter(lambda x: x, reader)
            return list(map(DataLoader.parse_line, filtered))
