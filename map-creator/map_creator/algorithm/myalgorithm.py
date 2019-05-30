import logging
from typing import List

from . import Algorithm
from .. import utils
from ..model import Map

LOGGER = logging.getLogger(__name__)


class MyAlgorithm(Algorithm):
    def __init__(self, ref_point: 'Coordinate', diff_distance: float, diff_heading: float):
        '''Create a MyAlgorithm instance

        Args:
            ref_point (Coordinate): the reference point
            diff_distance (float): maximum average distance difference between two mergeable paths (in kilometers)
            diff_heading (float): maximum average heading difference between two mergeable paths (in degrees)
        '''

        super().__init__(ref_point)

        self._diff_distance = diff_distance
        self._diff_heading = diff_heading

    def _average_distance(self, path1: 'Path', path2: 'Path') -> float:
        '''Calculates the average distance between the points of the two input paths.
        First calculates the average of the distances between the individual points of path1
        and all of the points of path2, then calculates the average of those distances.

        Args:
            path1 (Path): the first path
            path2 (Path): the second path

        Returns:
            float: the average distance between the points of the two paths
        '''

        avg_distances = []

        for point1 in path1.points:
            avg_distance = 0

            for point2 in path2.points:
                avg_distance += point1.position.distance(point2.position)

            if path2.points:
                avg_distance /= len(path2.points)

            avg_distances.append(avg_distance)

        return 0 if not avg_distances else sum(avg_distances) / len(avg_distances)

    def _average_heading(self, path: 'Path') -> float:
        '''Calculates the average heading of the path

        Args:
            path (Path): the path

        Returns:
            float: the average heading of the path
        '''

        headings = [point.heading for point in path.points]

        return 0 if not headings else sum(headings) / len(headings)

    def _is_mergeable(self, path1: 'Path', path2: 'Path') -> bool:
        '''Determines if two the input paths are mergeable based
        on the average distance between their points, their average
        headings and the self._diff_distance, self._diff_heading parameters

        Args:
            path1 (Path): the first path
            path2 (Path): the second path

        Returns:
            bool: whether the two paths are mergeable
        '''

        if type(path1) != type(path2):
            return False

        avg_distance = self._average_distance(path1, path2)

        avg_heading1 = self._average_heading(path1)
        avg_heading2 = self._average_heading(path2)

        return avg_distance <= self._diff_distance and \
            abs(avg_heading1 - avg_heading2) <= self._diff_heading

    def _merge(self, path1: 'Path', path2: 'Path') -> ('Path', 'Path'):
        '''Merge the two input paths if they are the same type.
        If they are ingress paths than the egresses are combined.
        The paths are merged into path1. The path2 is deleted.

        Args:
            path1 (Path): the first path
            path2 (Path): the second path

        Returns:
            (Path, Path): the two paths after the merge
        '''

        if type(path1) != type(path2):
            return (path1, path2)

        if type(path1) == Ingress:
            path1.egresses.extend(path2.egresses)

        return (path1, None)

    def process(self, paths: List['Path']) -> 'Map':
        '''Create map data from the input paths

        Args:
            paths (List[Path]): the paths

        Returns:
            Map: the created map data
        '''

        ingresses, egresses = [], []

        for path in paths:
            # split the path into ingress and egress parts
            split_point = utils.closest_point(self._ref_point, path.points)
            ingress, egress = utils.split_path(split_point, path)
            ingresses.append(ingress)
            egresses.append(egress)

        # calculate the average distance between
        # every two ingresses and every two egresses
        # merge ingresses and egresses

        LOGGER.debug(
            f'before merge: len(ingresses)={len(ingresses)}, len(egresses)={len(egresses)}')

        for arr in [ingresses, egresses]:
            for i in range(len(arr) - 1, -1, -1):
                if i >= len(arr):
                    break

                p1 = arr[i]

                for j in range(len(arr) - 1, -1, -1):
                    if i == j:
                        continue

                    p2 = arr[j]

                    # determine and merge if the two paths are mergeable
                    if self._is_mergeable(p1, p2):
                        p1, p2 = self._merge(p1, p2)
                        if not p2:
                            del arr[j]

        LOGGER.debug(
            f'after merge: len(ingresses)={len(ingresses)}, len(egresses)={len(egresses)}')

        # create and return map data
        mapdata = Map(self._ref_point, ingresses)
        return mapdata
