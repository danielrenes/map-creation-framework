from datetime import datetime
from threading import Lock

from .wrapper import WrappedMap


def non_blocking_lock(lock):
    def outer(function):
        def inner(*args, **kwargs):
            l = getattr(args[0], lock)
            if l.acquire(False):
                try:
                    return function(*args, **kwargs)
                finally:
                    l.release()
        return inner
    return outer


class Rsu:
    def __init__(self,
                 processor: 'Processor',
                 time_window_seconds: int = 60,
                 debug_server: 'DebugHTTPServer' = None):
        self.ref_point = processor._preprocessor._ref_point
        self.range_ = processor._preprocessor._range

        self.time_window = time_window_seconds
        self.last_update = datetime.utcnow()

        self.paths = []
        self.paths_lock = Lock()

        self._processor = processor
        self._debug_server = debug_server

        if self._debug_server:
            self._debug_server.rsu_info = {
                'ref_point': {
                    'latitude': self.ref_point.latitude,
                    'longitude': self.ref_point.longitude
                },
                'range': self.range_
            }

    @non_blocking_lock('paths_lock')
    def _update_paths(self):
        now = datetime.utcnow()

        for i in range(len(self.paths) - 1, -1, -1):
            path = self.paths[i]

            for j in range(len(path.points) - 1, -1, -1):
                point = path.points[j]

                if (now - point.timestamp).total_seconds() > self.time_window:
                    del path.points[j]

            if len(path.points) == 0:
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
        if self.elapsed_time() >= self.time_window:
            self.last_update = datetime.utcnow()
            self._update_paths()
            map_data = self._processor.process(self.paths)

            if self._debug_server:
                wrapped_map = WrappedMap(map_data)
                wrapped_map.truncate()
                self._debug_server.latest_map = wrapped_map.to_json()

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
