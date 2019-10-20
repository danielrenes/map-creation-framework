import csv
import json
import os
import re
import sys
from typing import List, Mapping, TextIO

from . import Closable

if 'SUMO_HOME' not in os.environ:
    raise RuntimeError('SUMO_HOME environment variable was not set')
SUMO_HOME = os.environ['SUMO_HOME']
sys.path.append(os.path.join(SUMO_HOME, 'tools'))

import traci    # noqa


class FeederObject:
    def __init__(self, identifier: int, latitude: float, longitude: float):
        self.identifier = identifier
        self.latitude = latitude
        self.longitude = longitude

    def encode(self):
        return f'{self.identifier}, {self.latitude}, {self.longitude}'

    def __repr__(self):
        return f'FeederObject(identifier={self.identifier}, latitude={self.latitude}, longitude={self.longitude}'


class Reader(Closable):
    def __init__(self, mapping: Mapping[str, str]):
        self.mapped_keys = ['identifier', 'latitude', 'longitude']
        self.mapping = mapping
        self.is_finished = False

        if mapping and not self.validate_mapping():
            raise ValueError(
                f'mapping must contain: {", ".join(key for key in self.mapped_keys)}')

    def validate_mapping(self) -> bool:
        if not hasattr(self, 'mapping'):
            return False

        return all(key in self.mapping for key in self.mapped_keys)

    def read(self) -> List[FeederObject]:
        if self.is_finished:
            print('finished')
            self.close()

        return self.get_next()

    def get_next(self) -> List[FeederObject]:
        raise NotImplementedError


class CsvReader(Reader):
    def __init__(self, mapping: Mapping[str, str], f: TextIO, delimiter: str):
        super().__init__(mapping)

        self.f = f
        self.reader = csv.reader(self.f, delimiter=delimiter)
        self.read_header()

    def read_header(self):
        try:
            cols = next(self.reader)
            for i, col in enumerate(cols):
                try:
                    idx = list(self.mapping.values()).index(col)
                    key = list(self.mapping.keys())[idx]
                    self.mapping[key] = i
                except ValueError:
                    pass
        except StopIteration:
            self.close()

    def read_line(self) -> FeederObject:
        try:
            cols = next(self.reader)
            id_, lat, lon = None, None, None

            for i, col in enumerate(cols):
                try:
                    idx = list(self.mapping.values()).index(i)
                    key = list(self.mapping.keys())[idx]

                    if key == 'identifier':
                        id_ = int(col)
                    elif key == 'latitude':
                        lat = float(col)
                    elif key == 'longitude':
                        lon = float(col)
                except ValueError:
                    pass

            if id_ and lat and lon:
                return FeederObject(id_, lat, lon)
        except StopIteration:
            self.is_finished = True
            return None

    def get_next(self) -> List[FeederObject]:
        return [self.read_line(), ]

    def close(self):
        if not self.f.closed:
            self.f.close()


class SumoReader(Reader):
    def __init__(self, sumocfg_path):
        super().__init__(None)

        self.end_time = self._get_end_time(sumocfg_path) * 1000

        sumo_binary = os.path.join(SUMO_HOME, 'bin', 'sumo')
        sumo_cmd = [sumo_binary, '-c', sumocfg_path]

        traci.start(sumo_cmd)

    def _get_end_time(self, sumocfg_path: str) -> int:
        with open(sumocfg_path, 'r') as f:
            content = f.read()

        match = re.search(r'<end value="(\d*)"/>', content)
        return int(match.group(1))

    def _pull_vehicles(self) -> List[FeederObject]:
        objs = []

        for vehicle_id in traci.vehicle.getIDList():
            x, y = traci.vehicle.getPosition(vehicle_id)
            lon, lat = traci.simulation.convertGeo(x, y)
            objs.append(FeederObject(vehicle_id, lat, lon))

        return objs

    def get_next(self) -> List[FeederObject]:
        if traci.simulation.getCurrentTime() > self.end_time:
            self.is_finished = True
            return

        traci.simulationStep()
        return self._pull_vehicles()

    def close(self):
        try:
            traci.close()
        except traci.exceptions.FatalTraCIError:
            pass
