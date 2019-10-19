import numpy as np

from utils import heatmap, annotate_heatmap


def create_heatmap(ax1, ax2, data, directory, n_cars, sim_time, algorithm):
    dataset = list(filter(lambda x: x['directory'] == directory
                          and x['number_of_cars'] == n_cars
                          and x['max_time'] == sim_time
                          and x['type'] == algorithm, data))

    dataset = [{k: v for k, v in item.items() if k not in
                ['directory', 'number_of_cars', 'max_time', 'type']} for item in dataset]

    if not dataset:
        return

    if algorithm == 'dbscan':
        xkey = 'eps'
        ykey = 'min_pts'
    elif algorithm == 'myalgorithm':
        xkey = 'diff_dist'
        ykey = 'diff_head'
    elif algorithm == 'hierarchical':
        xkey = 'strategy'
        ykey = 'measure'
    else:
        raise RuntimeException(f'Unknown algorithm {algorithm}')

    x_labels = {v for item in dataset for k, v in item.items() if k == xkey}
    y_labels = {v for item in dataset for k, v in item.items() if k == ykey}

    x_labels = sorted(list(x_labels))
    y_labels = sorted(list(y_labels), reverse=True)

    matrix = []
    matches_matrix = []
    duplicates_matrix = []

    for y_label in y_labels:
        row = []
        for x_label in x_labels:
            item = next(filter(lambda item: item.get(xkey) ==
                               x_label and item.get(ykey) == y_label, dataset))
            row.append(item)
        matrix.append(row)
        matches_matrix.append([item['matches'] for item in row])
        duplicates_matrix.append([item['duplicates'] for item in row])

    matches_matrix = np.array(matches_matrix)
    duplicates_matrix = np.array(duplicates_matrix)

    im1, _ = heatmap(matches_matrix, ykey, xkey, y_labels, x_labels,
                     ax=ax1, cmap="YlGn", cbarlabel="matches")
    annotate_heatmap(im1, valfmt="{x}")

    im2, _ = heatmap(duplicates_matrix, ykey, xkey, y_labels, x_labels,
                     ax=ax2, cmap="YlOrRd", cbarlabel="duplicates")
    annotate_heatmap(im2, valfmt="{x}")
