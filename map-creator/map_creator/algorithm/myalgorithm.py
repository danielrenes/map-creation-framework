import logging
from typing import Callable, List

from . import Algorithm
from .. import utils
from ..model import Ingress, Map, Point

LOGGER = logging.getLogger(__name__)


class MyAlgorithm(Algorithm):
    def __init__(self,
                 ref_point: 'Coordinate',
                 dist_func: Callable[['Path', 'Path'], float],
                 diff_distance: float,
                 diff_heading: float):
        '''Create a MyAlgorithm instance

        Args:
            ref_point (Coordinate): the reference point
            diff_distance (float): maximum average distance difference between two mergeable paths (in kilometers)
            diff_heading (float): maximum average heading difference between two mergeable paths (in degrees)
        '''

        super().__init__(ref_point, dist_func)

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

        path1 = utils.condense(path1)
        path2 = utils.condense(path2)

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

    def _process(self, paths: List['Path']) -> List['Path']:
        for i in range(len(paths)):
            if i >= len(paths):
                break

            for j in range(len(paths) - 1, -1, -1):
                if i >= len(paths):
                    break

                if i == j:
                    continue

                if self._is_mergeable(paths[i], paths[j]):
                    paths[i], _ = self._merge(paths[i], paths[j])
                    del paths[j]

        return paths

    def process_ingresses(self, ingresses: List['Ingress']) -> List['Ingress']:
        return self._process(ingresses)

    def process_egresses(self, egresses: List['Egress']) -> List['Egress']:
        return self._process(egresses)
