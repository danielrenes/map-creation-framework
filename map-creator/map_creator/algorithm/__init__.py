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
    def create(config: dict, ref_point: 'Coordinate') -> Algorithm:
        def invalid_args(*args) -> bool:
            return any([arg is None for arg in args])

        if ref_point is None:
            raise ValueError('ref_point must be configured')

        type_ = config.get('type')
        if not type_:
            raise ValueError('type must be configured')

        if type_ == 'dbscan':
            eps = config.get('eps')
            min_pts = config.get('min_pts')

            if invalid_args(eps, min_pts):
                raise ValueError(
                    'eps, min_pts must be configured for DBSCAN')

            return DBSCAN(ref_point, eps, min_pts)
        elif type_ == 'hierarchical':
            strategy = config.get('strategy')
            measure = config.get('measure')

            if invalid_args(strategy, measure):
                raise ValueError(
                    'strategy, measure must be configured for Hierarchical')

            # TODO
            return None
        elif type_ == 'myalgorithm':
            diff_dist = config.get('diff_dist')
            diff_head = config.get('diff_head')

            if invalid_args(diff_dist, diff_head):
                raise ValueError(
                    'diff_dist, diff_head must be configured for MyAlgorithm')

            return MyAlgorithm(ref_point, diff_dist, diff_head)
        else:
            raise ValueError(f'invalid type: {type_}')
