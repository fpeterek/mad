import pygame.display

from visualization.map import Map

from cluster_point import ClusterPoint


class Visualizer:
    def __init__(self, vis_map: Map, points: list[ClusterPoint]):
        self.map = vis_map

        ratio = self.map.img.get_height() / self.map.img.get_width()
        self.width = 1000
        self.height = int(self.width * ratio)

        self.screen = pygame.display.set_mode((self.width, self.height))
        self.map.scale_img(self.width, self.height)

        self.points: list[ClusterPoint] = points

        self.px = (self.map.right_bottom.lon - self.map.left_top.lon) / self.width
        self.py = (self.map.left_top.lat - self.map.right_bottom.lat) / self.height

        self.open = True

    def poll_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                self.open = False

    def redraw(self) -> None:
        self.screen.fill((255, 255, 255))

        self.screen.blit(self.map.img, self.map.img.get_rect())

        for point in self.points:
            pygame.draw.circle(self.screen, point.color, self.coords_to_cart(lat=point.lat, lon=point.lon), 3)

        pygame.display.flip()

    def coords_to_cart(self, lat: float, lon: float) -> tuple[float, float]:
        x = (lon - self.map.left_top.lon) / self.px
        y = self.height - (lat - self.map.right_bottom.lat) / self.py
        return x, y

    def update(self):
        self.poll_events()
        if self.open:
            self.redraw()

