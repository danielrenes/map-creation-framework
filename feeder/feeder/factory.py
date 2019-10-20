from typing import Tuple

from . import Mode
from .feeder import Feeder
from .generator import Generator
from .queue import Queue
from .reader import CsvReader, SumoReader


class Factory:
    @staticmethod
    def create(config: dict) -> Tuple['Queue', 'Runner']:
        reader = None

        mode_str = config.get('mode')

        if not mode_str:
            raise ValueError('mode must be configured')

        mode = Mode(mode_str)

        if mode not in list(Mode):
            raise ValueError(f'invalid mode: {mode}, options: {list(Mode)}')

        source = config.get('source')
        mapping = config.get('mapping')
        if not source:
            raise ValueError('source must be configured')

        if source == 'csv':
            if not mapping:
                raise ValueError('mode must be configured for CsvFeeder')

            filepath = config.get('filepath')
            delimiter = config.get('delimiter', ',')

            if not filepath:
                raise ValueError('filepath must be configured for CsvFeeder')

            f = open(filepath)
            reader = CsvReader(mapping, f, delimiter)
        elif source == 'sumo':
            sumocfg_path = config.get('sumocfg_path')

            if not sumocfg_path:
                raise ValueError(
                    'sumocfg_path must be configured for SumoFeeder')

            reader = SumoReader(sumocfg_path)
        elif source == 'json':
            pass
        else:
            raise ValueError(f'invalid source: {source}')

        if mode == Mode.FEED:
            queue = Queue()
            return (queue, Feeder(reader, queue))
        elif mode == Mode.GENERATE:
            return (None, Generator(reader, 'generated.out'))
