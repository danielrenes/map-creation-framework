import itertools
import math
from typing import Callable, List

from . import INFINITY
from .model import Coordinate, Point


def get_distance_function(dist_func: str) -> Callable[['Path', 'Path'], float]:
    if dist_func == 'euclidean':
        return euclidean
    elif dist_func == 'dtw':
        return dtw
    else:
        raise RuntimeError(f'Unknown distance function: {dist_func}')


def euclidean(path_1: 'Path', path_2: 'Path') -> float:
    if len(path_1.points) == 0 or len(path_2.points) == 0:
        return INFINITY

    distance = 0

    for p1, p2 in itertools.zip_longest(path_1.points, path_2.points, fillvalue=Point(None, Coordinate(0, 0))):
        distance += p1.position.distance(p2.position) ** 2

    return math.sqrt(distance)


def dtw(path_1: 'Path', path_2: 'Path') -> float:
    def _create_table(n: int, m: int) -> List[List[int]]:
        table = []
        for _ in range(n+1):
            table.append([INFINITY for _ in range(m+1)])
        table[0][0] = 0
        return table

    n = len(path_1.points)
    m = len(path_2.points)
    table = _create_table(n, m)
    for i in range(1, n+1):
        for j in range(1, m+1):
            coord_1 = path_1.points[i-1].position
            coord_2 = path_2.points[j-1].position
            table[i][j] = coord_1.distance(
                coord_2) + min(table[i-1][j-1], table[i][j-1], table[i-1][j])
    return table[n][m]
