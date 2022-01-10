import json

from data_loader import DataLoader
from cluster_point import ClusterPoint
from visualization.visualizer import Visualizer
from kmeans.kmeans import kmeans
from visualization.map import Map
from data.crime_record import CrimeRecord
from silhouette_index import silhouette_index


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
        'records_total': len(data),
    }
    crime_types = dict()
    highest_offenses = dict()
    streets = dict()
    districts = dict()
    months = dict()
    durations = dict()
    solved = dict()
    crime_data = dict()

    for record in data:
        crime_types[record.crime_type] = crime_types.get(record.crime_type, 0) + 1
        highest_offenses[record.highest_offense] = highest_offenses.get(record.highest_offense, 0) + 1
        street = parse_street(record.location if record.location else 'Unknown')
        streets[street] = streets.get(street, 0) + 1
        district = record.council_district if record.council_district else 'Unknown'
        districts[district] = districts.get(district, 0) + 1
        month = record.report_date.month
        months[month] = months.get(month, 0) + 1

        if record.is_cleared and record.clearance_time is not None:
            if record.crime_type not in durations:
                durations[record.crime_type] = []
            durations[record.crime_type].append(record.clearance_time)
            solved[record.crime_type] = solved.get(record.crime_type, 0) + 1

    for crime, duration_list in durations.items():
        solved_count = solved[crime]
        average_clearance_time = sum(duration_list) / solved_count
        sum_of_squares = 0
        for duration in duration_list:
            sum_of_squares += (average_clearance_time - duration) ** 2
        variance = sum_of_squares / solved_count
        std_dev = variance ** 0.5

        crime_data[crime] = {
            'count': crime_types[crime],
            'solved': solved_count,
            'average_clearance_time': average_clearance_time,
            'variance': variance,
            'standard_deviation': std_dev,
        }

    results['crime_types'] = crime_types
    results['highest_offenses'] = highest_offenses
    results['streets'] = streets
    results['districts'] = districts
    results['months'] = months
    results['crime_data'] = crime_data
    return results


def run(input_file: str, clusters: int, attempts: int, processes: int, sil_idx: bool, apply_kmeans: bool):
    print('loading data...')
    data = DataLoader.load_data(input_file)

    if apply_kmeans:
        print('preparing for k-means application...')
        geo_points = [record.coordinates for record in data if record.coordinates]
        print('clustering...')
        clusters = kmeans(geo_points, cluster_count=clusters, attempts=attempts, processes=processes)

    print('calculating statistics...')
    stats = calc_statistics(data)

    if sil_idx:
        print('calculating silhouette index...')
        stats['silhouette_index'] = silhouette_index(clusters)

    with open('output.json', 'w') as out:
        json.dump(stats, out, indent=4)

    if apply_kmeans:
        points = []
        global _colors
        for color, cluster in zip(_colors, clusters):
            for point in cluster:
                points.append(ClusterPoint(geo_point=point, color=color))
        vis = Visualizer(vis_map=Map.load_map('resources/austin.json'), points=points)

        while vis.open:
            vis.update()

