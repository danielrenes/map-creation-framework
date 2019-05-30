from .wrapper import WrappedMap


class Rsu:
    def __init__(self,
                 processor: 'Processor',
                 max_points_per_path: int = 15,
                 max_idle_cycles: int = 10,
                 debug_server: 'DebugHTTPServer' = None):
        self.ref_point = processor._preprocessor._ref_point
        self.range_ = processor._preprocessor._range

        # self.max_points_per_path = max_points_per_path
        # self.max_idle_cycles = max_idle_cycles
        self.paths = []

        self._processor = processor
        self._debug_server = debug_server

        # self._idle_cycles = {}

        if self._debug_server:
            self._debug_server.rsu_info = {
                'ref_point': {
                    'latitude': self.ref_point.latitude,
                    'longitude': self.ref_point.longitude
                },
                'range': self.range_
            }

    # def _update_paths(self):
    #     for i in range(len(self.paths) - 1, -1, -1):
    #         path_id = self.paths[i].id_
            # self._idle_cycles[path_id] += 1

            # if self._idle_cycles[path_id] >= self.max_idle_cycles:
            #     self.paths.pop(i)
            # else:
            #     while len(self.paths[i].points) > self.max_points_per_path:
            #         self.paths[i].points.pop(0)

    def add_path(self, path: 'Path'):
        self.paths.append(path)
        # self._idle_cycles[path.id_] = 0

    def add_point(self, index: int, point: 'Point'):
        if index >= len(self.paths):
            return
        self.paths[index].add_point(point)
        # self._idle_cycles[self.paths[index].id_] = 0

    def update(self):
        # print(f'len(paths)={len(self.paths)}')
        # for i, path in enumerate(self.paths):
        #     print(f'len(paths[{i}]={len(path.points)}')

        if (len(self.paths) == 25):
            with open('debug.txt', 'w') as f:
                for path in self.paths:
                    f.write(f'id={path.id_}\n')
                    for point in path.points:
                        f.write(f'{point.position.latitude}, {point.position.longitude}\n')

        # self._update_paths()
        map_data = self._processor.process(self.paths)

        if self._debug_server:
            wrapped_map = WrappedMap(map_data)
            self._debug_server.latest_map = wrapped_map.to_json()

    def open(self):
        if self._debug_server:
            self._debug_server.start()

    def close(self):
        if self._debug_server:
            self._debug_server.stop()
