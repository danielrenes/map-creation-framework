def create_line_chart(ax, data, directory, n_cars, sim_time, algorithm):
    dataset = list(filter(lambda x: x['directory'] == directory
                          and x['number_of_cars'] == n_cars
                          and x['max_time'] == sim_time
                          and x['type'] == algorithm, data))

    dataset = [{k: v for k, v in item.items() if k not in
                ['directory', 'number_of_cars', 'max_time', 'type', 'elapsed']} for item in dataset]

    if not dataset:
        return

    x = list(range(len(dataset)))
    y1 = [item['connections'] for item in dataset]
    y2 = [item['matches'] for item in dataset]
    y3 = [item['duplicates'] for item in dataset]

    dataset = [{k: v for k, v in item.items() if k not in
                ['connections', 'matches', 'duplicates']} for item in dataset]

    labels = [', '.join(f'{k}: {v}' for k, v in item.items())
              for item in dataset]

    cell_text = \
        list(map(list, zip(*[list(item.values()) for item in dataset])))

    rows = list(dataset[0].keys())

    ax.set_xticklabels([])

    l1, = ax.plot(x, y1, linewidth=6)
    l2, = ax.plot(x, y2, linewidth=6)
    l3, = ax.plot(x, y3, linewidth=6)

    for tick in ax.yaxis.get_major_ticks():
        tick.label.set_fontsize(16)

    for tick in ax.yaxis.get_minor_ticks():
        tick.label.set_fontsize(16)

    t = ax.table(cellText=cell_text,
                 rowLabels=rows,
                 cellLoc='center',
                 loc='bottom',
                 bbox=[0, -0.275, 1, 0.275])

    t.set_fontsize(16)
    t.scale(1, 1.55)

    ax.legend((l1, l2, l3), ('connections', 'matches', 'duplicates'),
              prop={'size': 14}, bbox_to_anchor=(1.225, 0.975))
