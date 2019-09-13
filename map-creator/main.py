import json
import time

from map_creator.algorithm import Factory as AlgorithmFactory
from map_creator.feeder import Factory as FeederFactory
from map_creator.model import Coordinate
from map_creator.processor import Preprocessor, Processor
from map_creator.rsu import Rsu
from map_creator.server import DebugHTTPServer


config_path = './config.json'


def read_config(path):
    with open(path, 'r') as f:
        return json.loads(f.read())


config = read_config(config_path)

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

    algorithm = AlgorithmFactory.create(config['algorithm'], ref_point)

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

    if 'rsu' in config and 'time_window_seconds' in config['rsu']:
        rsu.time_window = config['rsu']['time_window_seconds']

    if 'feeder' not in config:
        raise ValueError('feeder must be configured')

    feeder = FeederFactory.create(config['feeder'], rsu)

    try:
        rsu.open()
        feeder.open()

        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        pass
    finally:
        feeder.close()
        rsu.close()

        with open('result.json', 'w') as f:
            f.write(json.dumps(debug_server.latest_map))


if __name__ == '__main__':
    main()
