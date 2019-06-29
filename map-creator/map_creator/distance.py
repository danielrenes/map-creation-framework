from typing import Callable, List

from . import INFINITY


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
