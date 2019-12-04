from typing import List

from . import utils

from .model import Path


class Processor:
    def __init__(self, algorithm: 'Algorithm', ref_point: 'Coordinate', range_: float):
        '''Create a Processor instance

        Args:
            algorithm (Algorithm): the classification algorithm
            ref_point (Coordinate): the reference point
            range_ (float): maximum distance from the reference point (in kilometers)
        '''
        self._algorithm = algorithm
        self._ref_point = ref_point
        self._range = range_

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

    def process(self, paths: List['Path']) -> 'Map':
        '''Create map data from the input paths

        Args:
            paths (List[Path]): the paths

        Returns:
            Map: the created map data
        '''

        preprocessed_paths = self.preprocess(paths)
        map_data = self._algorithm.process(preprocessed_paths)
        return map_data

    def postprocess(self, aggregated_map: 'Map', latest_map: 'Map') -> 'Map':
        '''Create the new aggregated map based on the
        current aggregated map and the latest map.

        Args:
            aggregated_map (Map): the aggregated map
            latest_map (Map): the latest map

        Returns:
            Map: the new aggregated map
        '''

        max_diff = 0.2

        if not aggregated_map:
            return latest_map

        for ingress in latest_map.ingresses:
            matched = False

            for ingress2 in aggregated_map.ingresses:
                if utils.compare_paths(ingress, ingress2, self._algorithm.dist_func) < max_diff:
                    matched = True
                    break

            if not matched:
                aggregated_map.ingresses.append(ingress)
            else:
                for egress in ingress.egresses:
                    matched = False

                    for egress2 in ingress2.egresses:
                        if utils.compare_paths(egress, egress2, self._algorithm.dist_func) < max_diff:
                            matched = True
                            break

                    if not matched:
                        ingress2.egresses.append(egress)

        return aggregated_map
