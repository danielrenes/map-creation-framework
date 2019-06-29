from tests import NoLoggingTestCase

from map_creator.distance import dtw
from map_creator.model import Coordinate, Path, Point


class DistanceTest(NoLoggingTestCase):
    def test_dtw(self):
        path_1 = Path()
        path_1.add_point(Point(1, Coordinate(47.47176, 19.05178)))
        path_1.add_point(Point(1, Coordinate(47.47180, 19.05163)))
        path_1.add_point(Point(1, Coordinate(47.47181, 19.05146)))

        path_2 = Path()
        path_2.add_point(Point(2, Coordinate(47.47209, 19.05159)))
        path_2.add_point(Point(2, Coordinate(47.47198, 19.05153)))
        path_2.add_point(Point(2, Coordinate(47.47184, 19.05146)))

        dtw_dist = dtw(path_1, path_2)

        self.assertAlmostEqual(dtw_dist, 0.0641, 4)
