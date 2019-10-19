import matplotlib.pyplot as plt


def create_comparison_chart(data, directories, n_cars, sim_times, algorithms):
    d_values = []
    h_values = []
    m_values = []

    for i0 in directories:
        for i1 in n_cars:
            for i2 in sim_times:
                for i3 in algorithms:
                    dataset = list(filter(lambda x: x['directory'] == i0
                                          and x['number_of_cars'] == i1
                                          and x['max_time'] == i2
                                          and x['type'] == i3, data))
                    best_record = None

                    for item in dataset:
                        if best_record is None or item['matches'] > best_record['matches']:
                            best_record = item

                    value = {
                        'matches': best_record['matches'],
                        'duplicates': best_record['duplicates'],
                        'elapsed': best_record['elapsed']
                    }

                    if i3 == 'dbscan':
                        d_values.append(value)
                    elif i3 == 'hierarchical':
                        h_values.append(value)
                    elif i3 == 'myalgorithm':
                        m_values.append(value)
                    else:
                        raise RuntimeError(f'Unknown algorithm {i3}')

    fig = plt.figure(figsize=(48, 16))
    gs = fig.add_gridspec(nrows=3, ncols=3, hspace=0)

    if len(d_values) != len(h_values) or len(h_values) != len(m_values):
        raise RuntimeError('length is not correct')

    ax1 = fig.add_subplot(gs[0, 0])
    ax2 = fig.add_subplot(gs[1, 0])
    ax3 = fig.add_subplot(gs[2, 0])

    ax1.tick_params(labelsize=14)
    ax2.tick_params(labelsize=14)
    ax3.tick_params(labelsize=14)

    pos = list(range(len(d_values)))

    l1, = ax1.plot(pos, [item['matches'] for item in d_values], linewidth=8)
    l2, = ax1.plot(pos, [item['matches'] for item in h_values], linewidth=8)
    l3, = ax1.plot(pos, [item['matches'] for item in m_values], linewidth=8)
    ax1.set_ylabel('matches', fontsize=16, labelpad=8)

    ax2.plot(pos, [item['duplicates'] for item in d_values], linewidth=8)
    ax2.plot(pos, [item['duplicates'] for item in h_values], linewidth=8)
    ax2.plot(pos, [item['duplicates'] for item in m_values], linewidth=8)
    ax2.set_ylabel('duplicates', fontsize=16, labelpad=8)

    ax3.plot(pos, [item['elapsed'] for item in d_values], linewidth=8)
    ax3.plot(pos, [item['elapsed'] for item in h_values], linewidth=8)
    ax3.plot(pos, [item['elapsed'] for item in m_values], linewidth=8)
    ax3.set_ylabel('runtime', fontsize=16, labelpad=8)
    ax3.set_xticks([])

    plt.legend((l1, l2, l3), ('dbscan', 'hierarchical', 'myalgorithm'),
               loc=(0.225, -0.125), ncol=3, prop={'size': 16})

    plt.savefig('chart-cmp.png', bbox_inches='tight', dpi=100)

    plt.cla()
    plt.close(fig)
