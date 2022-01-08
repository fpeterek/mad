import json

from data_loader import DataLoader
from cluster_point import ClusterPoint
from visualization.visualizer import Visualizer
from kmeans.kmeans import kmeans
from visualization.map import Map
from data.crime_record import CrimeRecord


_colors = [
    (66, 135, 245), (66, 239, 245), (66, 245, 141), (239, 245, 66), (245, 176, 66),
    (245, 66, 66), (245, 66, 236)
]


def parse_street(address: str) -> str:
    index = 0
    while index < len(address) and (address[0].isspace() or address[0].isdigit()):
        index += 1
    return address[index:]


def calc_statistics(data: list[CrimeRecord]) -> dict:
    results = {
        'records_total': {len(data)},
    }
    crime_types = {}
    highest_offenses = {}
    streets = {}
    districts = {}
    months = {}

    for record in data:
        crime_types[record.crime_type] = crime_types.get(record.crime_type, 0) + 1
        highest_offenses[record.highest_offense] = highest_offenses.get(record.highest_offense, 0) + 1
        street = parse_street(street if street else 'Unknown')
        streets[street] = streets.get(street, 0) + 1
        district = record.council_district if record.council_district else 'Unknown'
        districts[district] = districts.get(district, 0) + 1
        month = record.report_date.month
        months[month] = months.get(month, 0) + 1

    results['crime_types'] = crime_types
    results['highest_offenses'] = highest_offenses
    results['streets'] = streets
    results['districts'] = districts
    results['months'] = months
    return results


def main():
    print('loading data...')
    data = DataLoader.load_data('in/austin.csv')
    print('data loaded...')
    geo_points = [record.coordinates for record in data if record.coordinates]
    print('clustering...')
    clusters = kmeans(geo_points, cluster_count=7, attempts=5, processes=4)
    points = []
    global _colors
    stats = calc_statistics(data)
    with open('output.json', 'w') as out:
        json.dump(stats, out)
    for color, cluster in zip(_colors, clusters):
        for point in cluster:
            points.append(ClusterPoint(geo_point=point, color=color))
    vis = Visualizer(vis_map=Map.load_map('resources/austin.json'), points=points)

    while vis.open:
        vis.update()


if __name__ == '__main__':
    main()
