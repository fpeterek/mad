from datetime import datetime

from crime_record import CrimeRecord
from geo_converter import GeoConverter


class DataLoader:
    def __init__(self):
        self.geo_converter = GeoConverter()

    def parse_line(self, line: str) -> CrimeRecord:
        split = line.split(',')
        key = int(split[0])
        district = int(split[1]) if split[1] else None
        highest_offense = split[2]
        crime_type = split[3]
        report_date = datetime.strptime(split[4], '%d-%b-%y').date()
        location = split[5] if split[5] else None
        coordinates = None
        if split[6] and split[7]:
            coordinates = self.geo_converter.convert(float(split[6]), float(split[7]))
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

    def load(self, filename: str) -> list[CrimeRecord]:
        with open(filename) as file:
            filtered = filter(lambda x: x and not x.isspace(), file)
            return list(map(self.parse_line, filtered))

    @staticmethod
    def load_data(filename: str) -> list[CrimeRecord]:
        loader = DataLoader()
        return loader.load(filename)
