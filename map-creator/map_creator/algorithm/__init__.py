from typing import List


class Algorithm:
    def __init__(self, ref_point: 'Coordinate'):
        self._ref_point = ref_point

    def process(self, paths: List['Path']) -> 'Map':
        raise NotImplementedError


from .dbscan import DBSCAN  # noqa
from .myalgorithm import MyAlgorithm    # noqa


class Factory:
    @staticmethod
    def create(config: dict) -> Algorithm:
        def invalid_args(*args) -> bool:
            return any([arg is None for arg in args])

        algorithm = None

        type_ = config.get('type')
        if not type_:
            raise ValueError('type must be configured')

        if type_ == 'dbscan':
            ref_point = config.get('ref_point')
            eps = config.get('eps')
            min_pts = config.get('min_pts')

            if invalid_args(ref_point, eps, min_pts):
                raise ValueError(
                    'ref_point, eps, min_pts must be configured for DBSCAN')

            algorithm = DBSCAN(ref_point, eps, min_pts)
        elif type_ == 'myalgorithm':
            ref_point = config.get('ref_point')
            diff_dist = config.get('diff_dist')
            diff_head = config.get('diff_head')

            if invalid_args(ref_point, diff_dist, diff_head):
                raise ValueError(
                    'ref_point, diff_dist, diff_head must be configured for MyAlgorithm')

            algorithm = MyAlgorithm(ref_point, diff_dist, diff_head)
        else:
            raise ValueError(f'invalid type: {type_}')

        return algorithm
