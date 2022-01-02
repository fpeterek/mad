from data_loader import DataLoader
from cluster_point import ClusterPoint
from visualizer import Visualizer
import kmeans
from map import Map


_colors = [
    (66, 135, 245), (66, 239, 245), (66, 245, 141), (239, 245, 66), (245, 176, 66),
    (245, 66, 66), (245, 66, 236)
]


def main():
    print('loading data...')
    data = DataLoader.load_data('in/austin.csv')
    print('data loaded...')
    geo_points = [record.coordinates for record in data if record.coordinates]
    print('clustering...')
    clusters = kmeans.kmeans(geo_points, 7, 5)
    points = []
    global _colors
    for color, cluster in zip(_colors, clusters):
        for point in cluster:
            points.append(ClusterPoint(geo_point=point, color=color))
    vis = Visualizer(vis_map=Map.load_map('resources/austin.json'), points=points)

    while vis.open:
        vis.update()


if __name__ == '__main__':
    main()
