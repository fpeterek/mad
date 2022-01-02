import geopy.distance


class GeoPoint:
    def __init__(self, lat: float, lon: float):
        self.lat = lat
        self.lon = lon

    @property
    def latlon(self):
        return self.lat, self.lon

    def __str__(self):
        return f'Point {{latitude={self.lat}, longitude={self.lon}}}'

    def __repr__(self):
        return str(self)

    def distance(self, other):
        return geopy.distance.distance(self.latlon, other.latlon).m
