from typing import List

from . import utils


class Preprocessor:
    def __init__(self, ref_point: 'Coordinate', range_: float, num_of_points: int):
        '''Create a Preprocessor instance

        Args:
            ref_point (Coordinate): the reference point
            range_ (float): maximum distance from the reference point (in kilometers)
            num_of_points (int): number of points in every path
        '''
        self._ref_point = ref_point
        self._range = range_
        self._num_of_points = num_of_points

    def filter_points(self, points: List['Point']) -> List['Point']:
        '''Filter out the points from the given input that are
        further than self._range away from the given ref_point

        Args:
            points (List[Point]): the input points

        Returns:
            List[Point]: the filtered input points that are not
                greater than self._range away from the ref_point
        '''
        return [p for p in points if self._ref_point.distance(p.position) <= self._range]

    def preprocess(self, paths: List['Path']) -> List['Path']:
        out_paths = []

        for path in paths:
            # filter the points in paths
            filtered_points = self.filter_points(path.points)

            if not filtered_points:
                continue

            path.points.clear()
            for point in filtered_points:
                path.add_point(point)

            # find the key points on path
            path = utils.find_key_points(path)
            out_paths.append(path)

        return out_paths


class Processor:
    def __init__(self, algorithm: 'Algorithm', preprocessor: 'Preprocessor'):
        '''Create a Processor instance

        Args:
            algorithm (Algorithm): the classification algorithm
            preprocessor (Preprocessor): the preprocessor to use for the input paths
        '''
        self._algorithm = algorithm
        self._preprocessor = preprocessor

    def process(self, paths: List['Path']) -> 'Map':
        '''Create map data from the input paths

        Args:
            paths (List[Path]): the paths

        Returns:
            Map: the created map data
        '''

        preprocessed_paths = self._preprocessor.preprocess(paths)
        map_data = self._algorithm.process(preprocessed_paths)
        return map_data
