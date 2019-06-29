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
                 max_points_per_path: int = 15,
                 max_idle_cycles: int = 10,
                 update_period: int = 30,
                 debug_server: 'DebugHTTPServer' = None):
        self.ref_point = processor._preprocessor._ref_point
        self.range_ = processor._preprocessor._range

        self.max_points_per_path = max_points_per_path
        self.max_idle_cycles = max_idle_cycles
        self.update_period = update_period
        self.last_update = datetime.utcnow()

        self.paths = []
        self.paths_lock = Lock()

        self._processor = processor
        self._debug_server = debug_server

        self._idle_cycles = {}

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
        for i in range(len(self.paths) - 1, -1, -1):
            path_id = self.paths[i].id_
            self._idle_cycles[path_id] += 1

            if self._idle_cycles[path_id] >= self.max_idle_cycles:
                self.paths.pop(i)
            else:
                while len(self.paths[i].points) > self.max_points_per_path:
                    self.paths[i].points.pop(0)

    @non_blocking_lock('paths_lock')
    def add_path(self, path: 'Path'):
        self.paths.append(path)
        self._idle_cycles[path.id_] = 0

    @non_blocking_lock('paths_lock')
    def add_point(self, index: int, point: 'Point'):
        if index >= len(self.paths):
            return
        self.paths[index].add_point(point)
        self._idle_cycles[self.paths[index].id_] = 0

    @non_blocking_lock('paths_lock')
    def update(self):
        if self.elapsed_time() >= self.update_period:
            print(self.paths)
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
        print(f'Elapsed: {elapsed} secs')
        return elapsed

    def open(self):
        if self._debug_server:
            self._debug_server.start()

    def close(self):
        if self._debug_server:
            self._debug_server.stop()
