from typing import List

from . import Algorithm
from .. import utils
from ..model import Egress, Ingress, Map, Path, Point

NEGLIGIBLE_DISTANCE = 0.005
INFINITE_DISTANCE = 1000


def signum(number: float) -> int:
    return 1 if number > 0 else -1 if number < 0 else 0


def average_heading(path: 'Path') -> float:
    return sum([point.heading for point in path.points]) / len(path.points)


def max_overlap(path_1: 'Path', path_2: 'Path') -> 'Path':
    overlap = Path()

    for point_1 in path_1.points:
        for point_2 in path_2.points:
            dist = point_1.position.distance(point_2.position)
            diff_heading = abs(point_1.heading - point_2.heading)

            if dist < NEGLIGIBLE_DISTANCE and diff_heading < 5 and point_1 not in overlap:
                overlap.add_point(point_1)

    return overlap


def distance(path_1: 'Path', path_2: 'Path') -> float:
    if not path_1.points and not path_2.points:
        return 0
    elif (not path_1.points and path_2.points) or \
            (path_1.points and not path_2.points):
        return INFINITE_DISTANCE

    path_1 = utils.condense(path_1)
    path_2 = utils.condense(path_2)

    return sum(point_1.position.distance(point_2.position)
               for point_1, point_2 in zip(path_1.points, path_2.points)) / len(path_1.points)

    # if not path_1.points and not path_2.points:
    #     return 0
    # elif (not path_1.points and path_2.points) or \
    #         (path_1.points and not path_2.points):
    #     return INFINITE_DISTANCE

    # overlap = max_overlap(path_1, path_2)
    # coeff = 1 - len(overlap.points) / len(path_1.points)

    # distances = []

    # for point_1 in path_1.points:
    #     for point_2 in path_2.points:
    #         d = point_1.position.distance(point_2.position)
    #         distances.append(d)

    # distances = sorted(distances)
    # size = len(distances)
    # n = int(size * 0.1)
    # distances = distances[n:size-n]
    # size = size - 2 * n

    # return sum(distances) / size * coeff


class _DBSCAN:
    def __init__(self, eps: float, min_pts: int):
        self.eps = eps
        self.min_pts = min_pts

        self.reset()

    def reset(self):
        self.clusters = []
        self.clustered = []

    def predict(self, dataset: List['Path']):
        for data in dataset:
            if self._is_member(data, self.clustered):
                continue

            neighbours = self._range_query(data, dataset)
            if len(neighbours) < self.min_pts:
                continue
            else:
                cluster = self._expand_cluster(data, dataset, neighbours)
                self.clusters.append(cluster)

    def _range_query(self, data: 'Path', dataset: List['Path']):
        neighbours = []
        for data2 in dataset:
            if distance(data, data2) <= self.eps:
                neighbours.append(data2)
        return neighbours

    def _expand_cluster(self, data: 'Path', dataset: List['Path'], neighbours: List['Path']):
        cluster = [data, ]
        self.clustered.append(data)

        for neighbour in neighbours:
            if self._is_member(neighbour, self.clustered):
                continue

            neighbours2 = self._range_query(neighbour, dataset)
            if len(neighbours2) >= self.min_pts:
                neighbours.extend(neighbours2)

            if not self._is_member(neighbour, self.clustered):
                cluster.append(neighbour)
                self.clustered.append(neighbour)

        return cluster

    def _is_member(self, data: 'Path', container: List['Path']):
        for item in container:
            if data == item:
                return True
        return False


class DBSCAN(Algorithm, _DBSCAN):
    def __init__(self, ref_point: 'Coordinate', eps: float, min_pts: int):
        Algorithm.__init__(self, ref_point)
        _DBSCAN.__init__(self, eps, min_pts)

    def _longest(self, cluster: List['Path'], default: 'Path' = None) -> 'Path':
        max_length = 0
        longest_path = None

        for path in cluster:
            length = path.length()

            if length > max_length:
                max_length = length
                longest_path = path

        if longest_path:
            return longest_path
        else:
            return default

    def process_ingresses(self, ingresses: List['Ingress']) -> List['Ingress']:
        self.reset()
        self.predict(ingresses)

        processed_ingresses = []

        for cluster in self.clusters:
            _egresses = []

            for ingress in cluster:
                _egresses.extend(ingress.egresses)

            # ingresses.append(Ingress.from_path(utils.combine_paths(cluster)))
            _ingress = self._longest(cluster, Ingress())
            _ingress.egresses = _egresses
            processed_ingresses.append(_ingress)

        return processed_ingresses

    def process_egresses(self, egresses: List['Egress']) -> List['Egress']:
        self.reset()
        self.predict(egresses)

        processed_egresses = []

        for cluster in self.clusters:
            # ingress.egresses.append(
            #     Egress.from_path(utils.combine_paths(cluster)))
            processed_egresses.append(self._longest(cluster, Egress()))

        return processed_egresses
