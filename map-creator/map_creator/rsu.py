from datetime import datetime
import logging
from threading import Lock

from .uuid import generate_uuid
from .wrapper import WrappedMap


LOGGER = logging.getLogger(__name__)


def non_blocking_lock(lock):
    def outer(function):
        def inner(*args, **kwargs):
            l = getattr(args[0], lock)
            if l.acquire(False):
                try:
                    return function(*args, **kwargs)
                finally:
                    l.release()
            else:
                LOGGER.error(f'Could not acquire lock: {lock}')
        return inner
    return outer


class Rsu:
    def __init__(self,
                 processor: 'Processor',
                 update_time: int = 60,
                 time_window: int = 120,
                 debug_server: 'DebugHTTPServer' = None):
        self.ref_point = processor._preprocessor._ref_point
        self.range_ = processor._preprocessor._range

        self.update_time = update_time
        self.time_window = time_window
        self.last_update = datetime.utcnow()

        self.paths = []
        self.paths_lock = Lock()

        self._processor = processor
        self._debug_server = debug_server

        self._uuid = generate_uuid()
        self._map = None

        if self._debug_server:
            self._debug_server.rsu_info = {
                'ref_point': {
                    'latitude': self.ref_point.latitude,
                    'longitude': self.ref_point.longitude
                },
                'range': self.range_
            }

    def _update_paths(self):
        now = datetime.utcnow()

        for i in range(len(self.paths) - 1, -1, -1):
            path = self.paths[i]

            for j in range(len(path.points) - 1, -1, -1):
                point = path.points[j]

                if (now - point.timestamp).total_seconds() > self.time_window:
                    LOGGER.debug(
                        f'Removed point {point.uuid} from path {path.uuid}')
                    del path.points[j]

            if len(path.points) == 0:
                LOGGER.debug(f'Removed path {self.paths[i].uuid}')
                del self.paths[i]

    @non_blocking_lock('paths_lock')
    def add_path(self, path: 'Path'):
        self.paths.append(path)

    @non_blocking_lock('paths_lock')
    def add_point(self, index: int, point: 'Point'):
        if index >= len(self.paths):
            return

        self.paths[index].add_point(point)

    @non_blocking_lock('paths_lock')
    def update(self):
        if not self.update_time or (self.elapsed_time() >= self.update_time):
            LOGGER.debug('Update')

            self.last_update = datetime.utcnow()

            if self.time_window is not None:
                LOGGER.debug('Update paths')
                self._update_paths()

            LOGGER.debug(f'len(paths)={len(self.paths)}')

            map_data = self._processor.process(self.paths)
            self._map = self._processor.postprocess(self._map, map_data)

            if self._debug_server:
                self._debug_server.latest_map = self.generated_map

    @property
    def generated_map(self):
        wrapped_map = WrappedMap(self._map)
        return wrapped_map.to_json()

    def elapsed_time(self):
        now = datetime.utcnow()
        elapsed = (now - self.last_update).total_seconds()
        return elapsed

    def open(self):
        if self._debug_server:
            self._debug_server.start()

    def close(self):
        if self._debug_server:
            self._debug_server.stop()

    def is_open(self):
        return self._debug_server is not None
