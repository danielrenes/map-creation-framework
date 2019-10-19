import json
import logging
import time
import os
import sys

from map_creator.algorithm import Factory as AlgorithmFactory
from map_creator.distance import get_distance_function
from map_creator.feeder import Factory as FeederFactory
from map_creator.model import Coordinate
from map_creator.processor import Preprocessor, Processor
from map_creator.rsu import Rsu
from map_creator.server import DebugHTTPServer

if os.getcwd().endswith('map-creation-framework'):
    os.chdir('map-creator')

config_path = './config.json'


def read_config(path):
    if sys.stdin.isatty():
        with open(path, 'r') as f:
            return json.loads(f.read())
    else:
        return json.loads(''.join(sys.stdin.readlines()))


config = read_config(config_path)

log_level = config.get('log_level', 'INFO')

logging.basicConfig(
    level=logging._nameToLevel[log_level],
    format='%(asctime)s %(funcName)-12s %(lineno)-4d %(levelname)-8s %(message)s'
)

debug = config.get('debug', False)

if 'reference_point' not in config \
        or 'latitude' not in config['reference_point'] \
        or 'longitude' not in config['reference_point']:
    raise ValueError(
        'reference_point must be configured with latitude and longitude')

ref_point = Coordinate(config['reference_point']['latitude'],
                       config['reference_point']['longitude'])


def main():
    if 'algorithm' not in config:
        raise ValueError('algorithm must be configured')

    dist_func = get_distance_function(config.get('dist_func', 'dtw'))

    algorithm = AlgorithmFactory.create(config['algorithm'],
                                        ref_point,
                                        dist_func)

    debug_server = None

    if debug:
        if 'debug_server' in config:
            host = config['debug_server'].get('host')
            port = config['debug_server'].get('port')

            debug_server = DebugHTTPServer(host, port)

    if 'preprocessor' not in config \
            or 'range' not in config['preprocessor'] \
            or 'num_points' not in config['preprocessor']:
        raise ValueError(
            'preprocessor must be configured with range and num_points')

    preprocessor = Preprocessor(ref_point,
                                config['preprocessor']['range'],
                                config['preprocessor']['num_points'])

    processor = Processor(algorithm, preprocessor)

    rsu = Rsu(processor, debug_server=debug_server)

    if 'rsu' in config:
        if 'update_time' in config['rsu']:
            if config['rsu']['update_time']['enabled']:
                rsu.update_time = config['rsu']['update_time']['value']
            else:
                rsu.update_time = None
        if 'time_window' in config['rsu']:
            if config['rsu']['time_window']['enabled']:
                rsu.time_window = config['rsu']['time_window']['value']
            else:
                rsu.time_window = None

    if 'feeder' not in config:
        raise ValueError('feeder must be configured')

    feeder = FeederFactory.create(config['feeder'], rsu)

    try:
        rsu.open()
        feeder.open()

        while rsu.is_open() or feeder.is_open():
            time.sleep(0.1)
    except KeyboardInterrupt:
        pass
    finally:
        feeder.close()
        rsu.close()

        with open('result.json', 'w') as f:
            f.write(json.dumps(rsu.generated_map))


if __name__ == '__main__':
    main()
