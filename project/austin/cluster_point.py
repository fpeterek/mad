from geo_point import GeoPoint


class ClusterPoint(GeoPoint):
    def __init__(self, geo_point: GeoPoint, color: tuple[int, int, int]):
        super().__init__(lat=geo_point.lat, lon=geo_point.lon)
        self.color = color
