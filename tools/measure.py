import csv
import itertools
import json
import os
import shutil
import subprocess
import time

feeder_config = {
    'mode': 'generate',
    'source': 'sumo',
    'mapping': {
        'identifier': 'id',
        'latitude': 'latitude',
        'longitude': 'longitude'
    },
    'sumocfg_path': None
}

creator_config = {
    'log_level': 'DEBUG',
    'algorithm': {},
    'debug': False,
    'feeder': {
        'type': 'file',
        'path': '/home/rd/Documents/Diplomamunka/0_FINAL/map-creation-framework/generated.out'
    },
    'preprocessor': {
        'range': 0.25,
        'num_points': 50
    },
    'reference_point': {},
    'rsu': {
        'time_window': {
            'enabled': True,
            'value': 5
        },
        'update_time': {
            'enabled': True,
            'value': 0.1
        }
    }
}

simulations = {
    'directory':            ['1'],  # , '2', '3', '4']
    'number_of_cars':       [100, 250, 500, 1000, 5000],
    'max_time':             [1000, 10000, 100000]
}

algorithms = [
    {
        'name':             'myalgorithm',
        'params': {
            'diff_dist':    [0.1, 0.2, 0.5],
            'diff_head':    [5, 10, 20]
        }
    },
    {
        'name':             'dbscan',
        'params': {
            'eps':          [0.05, 0.1, 0.25],
            'min_pts':      [1, 2, 5]
        }
    }
]


def print_with_time(message):
    now = time.strftime('%H:%M:%S', time.localtime())
    print(f'{now}  {message}')


def create_algorithm_configs():
    configs = []

    for algorithm in algorithms:
        name = algorithm['name']
        keys = list(algorithm['params'].keys())
        paramset = list(itertools.product(*list(algorithm['params'].values())))

        for params in paramset:
            config = ['type', name]

            for i, param in enumerate(params):
                config.append(keys[i])
                config.append(param)

            configs.append(config)

    return configs


def create_simulation_configs():
    configs = []

    keys = list(simulations.keys())
    paramset = list(itertools.product(*list(simulations.values())))

    for params in paramset:
        config = []

        for i, param in enumerate(params):
            config.append(keys[i])
            config.append(param)

        configs.append(config)

    return configs


def select_project_root_as_workdir():
    path = os.getcwd().split('map-creation-framework')[1]
    if path:
        for _ in range(len(path.split('/')[1:])):
            os.chdir('..')


def run_command_redirect_output_to_devnull(command):
    with open(os.devnull, 'w') as DEVNULL:
        proc = subprocess.Popen(command,
                                stdout=DEVNULL,
                                stderr=subprocess.STDOUT)
        proc.wait()

        if proc.returncode != 0:
            print_with_time(
                f'error: {" ".join(command)} returned {proc.returncode}')


def run_command_pipe_input_redirect_output_to_devnull(command, input_string):
    with open(os.devnull, 'w') as DEVNULL:
        proc = subprocess.Popen(command,
                                stdout=DEVNULL,
                                stdin=subprocess.PIPE,
                                stderr=subprocess.STDOUT)
        proc.communicate(input=input_string.encode('utf-8'))

        if proc.returncode != 0:
            print_with_time(
                f'error: {" ".join(command)} returned {proc.returncode}')


def create_simulation(simulation_config):
    directory = simulation_config[1]
    number_of_cars = simulation_config[3]
    max_time = simulation_config[5]

    select_project_root_as_workdir()
    os.chdir('simulations')

    run_command_redirect_output_to_devnull([
        './create.sh',
        str(directory),
        str(number_of_cars),
        str(max_time)
    ])

    print_with_time(f'simulation created with {simulation_config}')


def generate_feeder_data(simulations_dir):
    select_project_root_as_workdir()
    project_root_dir = os.getcwd()

    config = feeder_config.copy()
    config['sumocfg_path'] = f'{project_root_dir}/simulations/{simulations_dir}/map.sumocfg'

    os.chdir('feeder')

    run_command_pipe_input_redirect_output_to_devnull(
        ['python3', './main.py'],
        json.dumps(config))

    shutil.copyfile(f'{project_root_dir}/feeder/generated.out',
                    f'{project_root_dir}/generated.out')

    print_with_time(
        f'feeder data generated with {simulations_dir}/map.sumocfg')


def run_map_creator(simulations_dir, algorithm_config):
    select_project_root_as_workdir()

    with open(f'simulations/{simulations_dir}/ref_point.json') as f:
        ref_point = json.loads(f.read())

    config = creator_config.copy()
    config['reference_point'] = ref_point
    config['algorithm'] = {algorithm_config[i]: algorithm_config[i + 1]
                           for i in range(0, len(algorithm_config) - 1, 2)}

    os.chdir('map-creator')
    run_command_pipe_input_redirect_output_to_devnull(
        ['python3', './main.py'],
        json.dumps(config))

    print_with_time('map-creator finished')


def run_map_validator(simulations_dir):
    select_project_root_as_workdir()
    project_root_dir = os.getcwd()

    run_command_redirect_output_to_devnull([
        'java',
        '-jar',
        f'{project_root_dir}/map-validator/build/libs/map-validator-1.0-SNAPSHOT.jar',
        f'{project_root_dir}/map-creator/result.json',
        f'{project_root_dir}/simulations/{simulations_dir}/expected.json'
    ])

    print_with_time('map-validator finished')


def read_comparison():
    select_project_root_as_workdir()
    project_root_dir = os.getcwd()

    with open(f'{project_root_dir}/out/comp.json') as f:
        comp = json.loads(f.read())

    print_with_time('comparison result read')

    return comp


def create_result(simulation_config, algorithm_config, comparison_result):
    result = []

    for i in range(0, len(simulation_config) - 1, 2):
        result.append((simulation_config[i], simulation_config[i + 1]))

    for i in range(0, len(algorithm_config) - 1, 2):
        result.append((algorithm_config[i], algorithm_config[i + 1]))

    for key in sorted(comparison_result.keys()):
        result.append((key, comparison_result[key]))

    print_with_time('result record created')

    return result


def save_result(result):
    with open('results.csv', 'a') as f:
        csv_writer = csv.writer(f, delimiter=',', quotechar='"')

        record = []

        for field in result:
            record.append(field[0])
            record.append(field[1])

        csv_writer.writerow(record)

    print_with_time('saved result')


if __name__ == '__main__':
    simulation_configs = create_simulation_configs()
    algorithm_configs = create_algorithm_configs()

    for simulation_config in simulation_configs:
        create_simulation(simulation_config)
        generate_feeder_data(simulation_config[1])

        for algorithm_config in algorithm_configs:
            run_map_creator(simulation_config[1], algorithm_config)
            run_map_validator(simulation_config[1])
            comparison_result = read_comparison()

            result = create_result(simulation_config,
                                   algorithm_config,
                                   comparison_result)

            save_result(result)

            print_with_time(f'finished {algorithm_config}')

        print_with_time(f'finished {simulation_config}')
