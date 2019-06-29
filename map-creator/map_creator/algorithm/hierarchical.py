from enum import Enum
from typing import List

from . import Algorithm
from .. import INFINITY
from ..distance import dtw


class Strategy(Enum):
    TOP_DOWN = 0,
    BOTTOM_UP = 1


class DistanceMeasure(Enum):
    SINGLE_LINKAGE = 0,
    COMPLETE_LINKAGE = 1,
    AVERAGE_LINKAGE = 2


class Hierarchical(Algorithm):
    def __init__(self,
                 ref_point: 'Coordinate',
                 strategy: Strategy,
                 distance_measure: DistanceMeasure):

        Algorithm.__init__(self, ref_point)
        self._strategy = strategy
        self._distance_measure = distance_measure

    def process(self, paths: List['Path']) -> 'Map':
        clusters = self.create_clusters()

    def create_clusters(self, paths: List['Path']) -> List[List['Path']]:
        if self._strategy == Strategy.TOP_DOWN:
            return self.cluster_top_down(paths)
        elif self._strategy == Strategy.BOTTOM_UP:
            return self.cluster_bottom_up(paths)
        else:
            raise RuntimeError(f'Invalid strategy: {self._strategy}')

    def calculate_distance(self, cluster_1: List['Path'], cluster_2: List['Path']) -> float:
        if self._distance_measure == DistanceMeasure.SINGLE_LINKAGE:
            return self.single_linkage(cluster_1, cluster_2)
        elif self._distance_measure == DistanceMeasure.COMPLETE_LINKAGE:
            return self.complete_linkage(cluster_1, cluster_2)
        elif self._distance_measure == DistanceMeasure.AVERAGE_LINKAGE:
            return self.average_linkage(cluster_1, cluster_2)
        else:
            raise RuntimeError(
                f'Invalid distance measure: {self._distance_measure}')

    def cluster_top_down(self, paths: List['Path']) -> List[List['Path']]:
        clusters = [paths, ]
        # TODO
        return NotImplemented

    def cluster_bottom_up(self, paths: List['Path']) -> List[List['Path']]:
        # TODO return the history and the linkage values
        clusters = [[path, ] for path in paths]
        while len(clusters) > 1:
            min_dist = INFINITY
            min_i = None
            min_j = None
            for i in range(len(clusters)):
                for j in range(len(clusters)):
                    if i == j:
                        continue
                    dist = self.calculate_distance(clusters[i], clusters[j])
                    if min_dist > dist:
                        min_dist = dist
                        min_i = i
                        min_j = j
            new_cluster = [path for path in clusters[i] for i in [min_i, min_j]]
            if min_j > min_i:
                clusters.pop(min_j)
                clusters.pop(min_i)
            else:
                clusters.pop(min_i)
                clusters.pop(min_j)
            clusters.append(new_cluster)
        return clusters

    def single_linkage(self, cluster_1: List['Path'], cluster_2: List['Path']) -> float:
        min_dist = INFINITY
        for path_1 in cluster_1:
            for path_2 in cluster_2:
                dist = dtw(path_1, path_2)
                if dist < min_dist:
                    min_dist = dist
        return min_dist

    def complete_linkage(self, cluster_1: List['Path'], cluster_2: List['Path']) -> float:
        max_dist = 0
        for path_1 in cluster_1:
            for path_2 in cluster_2:
                dist = dtw(path_1, path_2)
                if dist > max_dist:
                    max_dist = dist
        return max_dist

    def average_linkage(self, cluster_1: List['Path'], cluster_2: List['Path']) -> float:
        distances = []
        for path_1 in cluster_1:
            for path_2 in cluster_2:
                dist = dtw(path_1, path_2)
                distances.append(dist)
        if distances:
            return sum(distances) / len(distances)
        else:
            return 0
