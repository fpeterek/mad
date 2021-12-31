import pyproj

from geo_point import GeoPoint


class GeoConverter:
    def __init__(self):
        self.fips4203 = pyproj.Proj('+proj=lcc +lat_1=30.11666666666667 +lat_2=31.88333333333333 '
                                    '+lat_0=29.66666666666667 +lon_0=-100.3333333333333 +x_0=700000 +y_0=3000000 '
                                    '+datum=NAD83 +units=us-ft +no_defs')
        self.wgs84 = pyproj.Proj("+init=EPSG:4326")

    def convert(self, x, y) -> GeoPoint:
        lon, lat = pyproj.transform(self.fips4203, self.wgs84, x, y)
        return GeoPoint(lat=lat, lon=lon)

