import json
import time

from map_creator.algorithm import Factory as AlgorithmFactory
from map_creator.feeder import FileFeeder, UdpFeeder
from map_creator.model import Coordinate
from map_creator.processor import Preprocessor, Processor
from map_creator.rsu import Rsu
from map_creator.server import DebugHTTPServer

debug = True

ref_point = Coordinate(47.476123, 19.053197)

config = {
    'algorithm': {
        'type': 'dbscan',
        'eps': 0.04,
        'min_pts': 0,
        'ref_point': ref_point
    },
    'debug_server': {
        'host': 'localhost',
        'port': 31289
    },
    'preprocessor': {
        'ref_point': ref_point,
        'range': 0.2,
        'num_points': 10
    }
}


def main():
    algorithm = AlgorithmFactory.create(config['algorithm'])

    debug_server = DebugHTTPServer() if debug else None

    preprocessor = Preprocessor(config['preprocessor']['ref_point'],
                                config['preprocessor']['range'],
                                config['preprocessor']['num_points'])

    processor = Processor(algorithm, preprocessor)

    rsu = Rsu(processor, debug_server=debug_server)

    # TODO: feeder params will be configurable

    feeder = FileFeeder(rsu, '../out')

    try:
        feeder.open()
        rsu.open()

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
