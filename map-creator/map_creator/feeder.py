import logging
import socket
import time
import threading
from typing import Tuple

from .model import Coordinate, Path, Point

LOGGER = logging.getLogger(__name__)


class Factory:
    @staticmethod
    def create(config: dict, rsu: 'Rsu'):
        type_ = config.get('type')

        if not type_:
            raise ValueError('type must be configured')

        if type_ == 'file':
            path = config.get('path')

            if not path:
                raise ValueError('path must be configured for FileFeeder')

            return FileFeeder(rsu, path)
        elif type_ == 'udp':
            host = config.get('host')
            port = config.get('port')
            server_host = config.get('server_host')
            server_port = config.get('server_port')

            return UdpFeeder(rsu, host, port, server_host, server_port)
        else:
            raise ValueError(f'invalid type: {type_}')


class Feeder:
    def __init__(self, rsu: 'Rsu'):
        self.rsu = rsu

    def open(self):
        raise NotImplementedError

    def close(self):
        raise NotImplementedError

    def decode(self, item: str) -> Tuple[str, float, float]:
        id_, lat, lon = item.split(',')
        id_ = str(id_)
        lat = float(lat)
        lon = float(lon)
        return (id_, lat, lon)

    def feed_one(self, data: str):
        id_, lat, lon = self.decode(data)

        coordinate = Coordinate(lat, lon)
        point = Point(id_, coordinate)
        distance = coordinate.distance(self.rsu.ref_point)

        if distance > self.rsu.range_:
            LOGGER.info(f'Out of range: {distance} > {self.rsu.range_}')
            return

        is_found = False

        for index, path in enumerate(self.rsu.paths):
            if id_ == path.id_:
                self.rsu.add_point(index, point)
                self.rsu.update()
                is_found = True
                break

        if not is_found:
            path = Path()
            path.add_point(point)
            self.rsu.add_path(path)
            self.rsu.update()


class FileFeeder(Feeder):
    def __init__(self, rsu: 'Rsu', in_file: str):
        super().__init__(rsu)
        self.in_file = in_file
        self.f = None

        LOGGER.info(f'File feeder initialized with filepath [{self.in_file}]')

    def open(self):
        LOGGER.info('Started File feeder')

        self.f = open(self.in_file, 'r')
        self.feed()

    def close(self):
        if self.f:
            self.f.close()

        LOGGER.info('Stopped File feeder')

    def feed(self):
        for line in self.f:
            self.feed_one(line)
        self.close()


class UdpFeeder(Feeder):
    def __init__(self, rsu: 'Rsu', host: str = 'localhost', port: int = 43256,
                 server_host: str = 'localhost', server_port: int = 51836):
        super().__init__(rsu)

        if not host:
            host = 'localhost'

        if not port:
            port = 43256

        if not server_host:
            server_host = 'localhost'

        if not server_port:
            server_port = 51836

        self.server_addr = (server_host, server_port)
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.setblocking(0)
        self.sock.bind((host, port))
        self.client_thread = threading.Thread(target=self.run_client_thread)
        self.client_thread.daemon = True
        self.stop_event = threading.Event()

        LOGGER.info(f'UDP feeder initialized on {host}:{port}')

    def run_client_thread(self):
        is_connected = False

        while not is_connected:
            try:
                self.sock.sendto(b'connect', self.server_addr)
                is_connected = True
            except BlockingIOError:
                LOGGER.error(
                    f'Could not connect to {self.server_addr}. Retry in 10 seconds.')
                time.sleep(10)

        LOGGER.info(f'Connected to {self.server_addr}')

        while not self.stop_event.is_set():
            try:
                data, _ = self.sock.recvfrom(1024)

                if not data:
                    LOGGER.info('Nothing was received, exiting...')
                    self.stop_event.set()
                else:
                    LOGGER.info(f'Received message: {data}')
                    self.feed(data)
            except BlockingIOError:
                pass

            time.sleep(0.1)

        try:
            self.sock.sendto(b'disconnect', self.server_addr)
            is_connected = False
        except BlockingIOError:
            pass

        if not is_connected:
            LOGGER.info(f'Disconnected from {self.server_addr}')
        else:
            LOGGER.warning(f'Could not disconnect from {self.server_addr}')

    def open(self):
        self.client_thread.start()
        LOGGER.info('Started UDP feeder')

    def close(self):
        self.stop_event.set()
        self.client_thread.join()
        LOGGER.info('Stopped UDP feeder')

    def feed(self, data: bytes):
        for item in self.split_list(data):
            self.feed_one(self.decode_item(item))

    def split_list(self, data: bytes) -> str:
        return data.decode().split('",')

    def decode_item(self, data: str) -> str:
        return data.replace('[', '').replace('"', '').replace(']', '')
