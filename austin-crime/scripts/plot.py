import os

import matplotlib.pyplot as plt


_months = ['Unknown', 'January', 'February', 'March', 'April', 'May', 'June', 'July', 'August',
           'September', 'October', 'November', 'December']


_clearance_status = {
    '': 'Unknown',
    'C': 'Arrest',
    'O': 'Exception',
    'N': 'Not cleared'
}


def load_folder(folder):
    csvs = [f'{folder.rstrip("/")}/{file}' for file in os.listdir(folder) if file.endswith('.csv')]
    lines = []
    for file in csvs:
        with open(file) as f:
            lines += [line.split(',') for line in f if line and not line.isspace()]
    return lines


def simple_bar_plot(labels, values):
    plt.bar(labels, values)
    plt.draw()
    plt.show()


def unzip(data) -> tuple[list, list[int]]:
    labels = [label for label, _ in data]
    values = [int(float(value)) for _, value in data]
    return labels, values


def kv_bar_plot(folder, asc=True, cap=None):
    data = load_folder(folder)
    data.sort(key=lambda pair: pair[1], reverse=not asc)
    labels, values = unzip(data)

    if cap is not None:
        labels = labels[:cap]
        values = values[:cap]

    simple_bar_plot(labels, values)


def plot_best_streets():
    kv_bar_plot('out/bestStreets')


def plot_worst_streets():
    kv_bar_plot('out/worstStreets', asc=False)


def plot_clearance_months():
    global _months

    data = load_folder('out/mostCommonClearanceMonth')
    data = [(int(m) if m != '""' else 0, int(c)) for m, c in data]
    data.sort(key=lambda pair: pair[0])
    labels, values = unzip(data)
    labels = [_months[i] for i in labels]
    simple_bar_plot(labels, values)


def plot_most_common_districts():
    data = load_folder('out/mostCommonDistrict')
    data = [(d if d != '""' else 'Unknown', int(c)) for d, c in data]
    data.sort(key=lambda pair: pair[1], reverse=True)
    labels, values = unzip(data)
    simple_bar_plot(labels, values)


def plot_most_common_offense():
    kv_bar_plot('out/mostCommonOffense', asc=False, cap=10)


def plot_least_common_offense():
    kv_bar_plot('out/mostCommonOffense', asc=True, cap=10)


def plot_highest_clearance_times():
    kv_bar_plot('out/topClearanceTimes', asc=False)


def plot_crime_solved_ratio():
    data = load_folder('out/solvedByCrime')
    data = [(record[0], int(float(record[3]) * 100)) for record in data]
    data.sort(key=lambda pair: pair[1], reverse=True)
    labels, values = unzip(data)
    simple_bar_plot(labels, values)


def plot_avg_clearance_time_by_crime():
    kv_bar_plot('out/clearanceByCrime')


def plot_crime_counts():
    kv_bar_plot('out/mostCommonCrime', asc=False)


def most_common_month_by_crime():
    global _months

    data = load_folder('out/mostCommonMonth')
    data = [(int(m) if m != '""' else 0, int(c)) for m, c in data]
    data.sort(key=lambda pair: pair[0])
    labels, values = unzip(data)
    labels = [_months[i] for i in labels]
    simple_bar_plot(labels, values)


def plot_clearance_status():
    global _clearance_status

    data = load_folder('out/mostCommonStatus')
    data = [(d if d != '""' else '', int(c)) for d, c in data]
    data.sort(key=lambda pair: pair[1], reverse=True)
    labels, values = unzip(data)
    labels = [_clearance_status[label] for label in labels]
    simple_bar_plot(labels, values)


def plot_slaughter_lane_crimes():
    kv_bar_plot('out/slaughterLaneType', asc=False)


def plot_offenses_against_children():
    data = load_folder('out/mostCommonOffense')
    data = [(d, int(c)) for d, c in data if 'CHILD' in d]
    data.sort(key=lambda pair: pair[1], reverse=True)
    labels, values = unzip(data)
    simple_bar_plot(labels, values)


def main():
    plot_offenses_against_children()
    plot_best_streets()
    plot_worst_streets()
    plot_clearance_months()
    plot_most_common_districts()
    plot_most_common_offense()
    plot_least_common_offense()
    plot_highest_clearance_times()
    plot_crime_solved_ratio()
    plot_avg_clearance_time_by_crime()
    plot_crime_counts()
    most_common_month_by_crime()
    plot_clearance_status()
    plot_slaughter_lane_crimes()


if __name__ == '__main__':
    main()
