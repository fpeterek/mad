import json

import pygame.image

from data.geo_point import GeoPoint


class Map:
    def __init__(self, img: pygame.surface.Surface, left_top: GeoPoint, right_bottom: GeoPoint):
        self.img = img
        self.left_top = left_top
        self.right_bottom = right_bottom

    @staticmethod
    def load_map(filename):
        with open(filename) as f:
            j = json.load(f)
            img = pygame.image.load(j['img'])

            left_top = j['left_top']
            right_bottom = j['right_bottom']
            left_top = GeoPoint(lat=float(left_top['lat']), lon=float(left_top['lon']))
            right_bottom = GeoPoint(lat=float(right_bottom['lat']), lon=float(right_bottom['lon']))

            return Map(img, left_top, right_bottom)

    def scale_img(self, width, height):
        self.img = pygame.transform.scale(self.img, (width, height)).convert()

