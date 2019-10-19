import numpy as np
import matplotlib.pyplot as plt


def create_algorithm_comparison_chart(algorithms, data, directory, n_cars, sim_time):
    def stats(values):
        arr = np.asarray(values)
        return (np.mean(arr), np.std(arr))

    dataset = list(filter(lambda x: x['directory'] == directory
                          and x['number_of_cars'] == n_cars
                          and x['max_time'] == sim_time, data))

    dataset = [{k: v for k, v in item.items() if k not in
                ['directory', 'number_of_cars', 'max_time']} for item in dataset]

    if not dataset:
        return

    matches = {}
    duplicates = {}
    runtimes = {}

    for algorithm in algorithms:
        records = [item for item in dataset if item['type'] == algorithm]
        _matches = [record['matches'] for record in records]
        _duplicates = [record['duplicates'] for record in records]
        _runtimes = [record['elapsed'] for record in records]

        matches[algorithm] = _matches
        duplicates[algorithm] = _duplicates
        runtimes[algorithm] = _runtimes

    mean_std_deviation = {}

    for algorithm in algorithms:
        msd_matches = stats(matches[algorithm])
        msd_duplicates = stats(duplicates[algorithm])
        msd_runtimes = stats(runtimes[algorithm])

        mean_std_deviation[algorithm] = {
            'matches': msd_matches,
            'duplicates': msd_duplicates,
            'runtimes': msd_runtimes
        }

    labels = algorithms
    x_pos = list(range(len(labels)))
    keys = ['matches', 'duplicates', 'runtimes']

    fig = plt.figure(figsize=(6, 8))
    gs = fig.add_gridspec(nrows=3, ncols=1, hspace=0)

    ax1 = fig.add_subplot(gs[0, 0])
    ax2 = fig.add_subplot(gs[1, 0])
    ax3 = fig.add_subplot(gs[2, 0])

    ax1.tick_params(labelsize=10)
    ax2.tick_params(labelsize=10)
    ax3.tick_params(labelsize=10)

    axes = [ax1, ax2, ax3]
    colors = ['green', 'red', 'blue']

    for ax, color, key in zip(axes, colors, keys):
        values = [mean_std_deviation[algorithm][key][0]
                  for algorithm in algorithms]
        errors = [mean_std_deviation[algorithm][key][1]
                  for algorithm in algorithms]

        ax.bar(x_pos, values, yerr=errors, align='center', color=color, alpha=0.35,
               ecolor='black', capsize=3, error_kw={'elinewidth': 2, 'markeredgewidth': 2})
        ax.set_ylabel(key, fontsize=10, labelpad=6)
        ax.set_xticks(x_pos)
        ax.set_xticklabels(labels)

    plt.savefig(f'chart-{directory}-{n_cars}-{sim_time}-cmp.png',
                bbox_inches='tight', dpi=100)
    plt.cla()
    plt.close(fig)
