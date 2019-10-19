#!/usr/bin/env python

import matplotlib.pyplot as plt

from line_chart import create_line_chart
from heatmap import create_heatmap
from algorithm_comparison import create_algorithm_comparison_chart
from comparison import create_comparison_chart


def read_results():
    data = []

    with open('results.csv', 'r') as f:
        for line in f:
            entry = {}
            columns = line.strip().split(',')

            for i in range(0, len(columns) - 1, 2):
                k, v = columns[i], columns[i + 1]

                try:
                    v = int(v)
                except ValueError:
                    try:
                        v = float(v)
                    except ValueError:
                        pass

                entry[k] = v

            data.append(entry)

    return data


def get_data_by_keys(data, keys):
    ret = []
    for key in keys:
        ret.append(list({item[key] for item in data}))
    return ret


data = read_results()

directories, n_cars, sim_times, algorithms = \
    get_data_by_keys(data, ['directory', 'number_of_cars', 'max_time', 'type'])

create_comparison_chart(data, directories, n_cars, sim_times, algorithms)

for i0 in directories:
    for i1 in n_cars:
        for i2 in sim_times:
            create_algorithm_comparison_chart(algorithms, data, i0, i1, i2)
            for i3 in algorithms:
                fig = plt.figure(figsize=(12, 9))

                gs = fig.add_gridspec(nrows=2,
                                      ncols=2,
                                      hspace=0.55,
                                      height_ratios=[7, 6])

                ax1 = fig.add_subplot(gs[0, :])
                ax2 = fig.add_subplot(gs[1, 0])
                ax3 = fig.add_subplot(gs[1, 1])

                create_line_chart(ax1, data, i0, i1, i2, i3)
                create_heatmap(ax2, ax3, data, i0, i1, i2, i3)

                plt.savefig(f'chart-{i0}-{i1}-{i2}-{i3}.png',
                            bbox_inches='tight', dpi=100)

                plt.cla()
                plt.close(fig)
