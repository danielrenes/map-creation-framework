from typing import Tuple

from .feeder import CsvFeeder, Feeder, SumoFeeder
from .queue import Queue


class Factory:
    @staticmethod
    def create(config: dict) -> Tuple[Queue, Feeder]:
        queue = Queue()
        feeder = None

        source = config.get('source')
        mapping = config.get('mapping')
        if not source or not mapping:
            raise ValueError('source and mapping must be configured')

        if source == 'csv':
            filepath = config.get('filepath')
            delimiter = config.get('delimiter', ',')

            if not filepath:
                raise ValueError('filepath must be configured for CsvFeeder')

            f = open(filepath)
            feeder = CsvFeeder(mapping, queue, f, delimiter)
        elif source == 'sumo':
            sumocfg_path = config.get('sumocfg_path')

            if not sumocfg_path:
                raise ValueError(
                    'sumocfg_path must be configured for SumoFeeder')

            feeder = SumoFeeder(mapping, queue, sumocfg_path)
        elif source == 'json':
            pass
        else:
            raise ValueError(f'invalid source: {source}')

        return (queue, feeder)
