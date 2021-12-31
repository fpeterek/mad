import geopy.distance


class GeoPoint:
    def __init__(self, lat: float, lon: float):
        self.lat = lat
        self.lon = lon

    @property
    def latlon(self):
        return self.lat, self.lon

    def distance(self, other):
        return geopy.distance.distance(self.latlon, other.latlon)
