from tests import NoLoggingTestCase
from map_creator.algorithm.dbscan import DBSCAN
from map_creator.distance import dtw
from map_creator.model import Coordinate, Path, Point


class DBSCANTest(NoLoggingTestCase):
    def setUp(self):
        ref_point = Coordinate(50.07005, 19.90398)
        eps = 0.025
        min_pts = 0
        self.algorithm = DBSCAN(ref_point, dtw, eps, min_pts)

    def test_process(self):
        path_1 = Path()
        path_1.add_point(Point(1, Coordinate(50.06984, 19.90552)))
        path_1.add_point(Point(1, Coordinate(50.06989, 19.90534)))
        path_1.add_point(Point(1, Coordinate(50.06993, 19.90513)))
        path_1.add_point(Point(1, Coordinate(50.06997, 19.90486)))
        path_1.add_point(Point(1, Coordinate(50.07001, 19.90461)))
        path_1.add_point(Point(1, Coordinate(50.07006, 19.90436)))
        path_1.add_point(Point(1, Coordinate(50.07009, 19.90415)))
        path_1.add_point(Point(1, Coordinate(50.07013, 19.90394)))
        path_1.add_point(Point(1, Coordinate(50.07016, 19.90371)))
        path_1.add_point(Point(1, Coordinate(50.07020, 19.90348)))
        path_1.add_point(Point(1, Coordinate(50.07023, 19.90321)))

        path_2 = Path()
        path_2.add_point(Point(2, Coordinate(50.07056, 19.90416)))
        path_2.add_point(Point(2, Coordinate(50.07049, 19.90413)))
        path_2.add_point(Point(2, Coordinate(50.07040, 19.90408)))
        path_2.add_point(Point(2, Coordinate(50.07034, 19.90404)))
        path_2.add_point(Point(2, Coordinate(50.07025, 19.90399)))
        path_2.add_point(Point(2, Coordinate(50.07014, 19.90395)))
        path_2.add_point(Point(2, Coordinate(50.07007, 19.90392)))
        path_2.add_point(Point(2, Coordinate(50.06999, 19.90388)))
        path_2.add_point(Point(2, Coordinate(50.06992, 19.90385)))
        path_2.add_point(Point(2, Coordinate(50.06983, 19.90381)))
        path_2.add_point(Point(2, Coordinate(50.06975, 19.90378)))

        path_3 = Path()
        path_3.add_point(Point(3, Coordinate(50.06964, 19.90387)))
        path_3.add_point(Point(3, Coordinate(50.06983, 19.90395)))
        path_3.add_point(Point(3, Coordinate(50.06997, 19.90401)))
        path_3.add_point(Point(3, Coordinate(50.07012, 19.90408)))
        path_3.add_point(Point(3, Coordinate(50.07029, 19.90416)))
        path_3.add_point(Point(3, Coordinate(50.07044, 19.90421)))

        path_4 = Path()
        path_4.add_point(Point(4, Coordinate(50.07012, 19.90307)))
        path_4.add_point(Point(4, Coordinate(50.07009, 19.90331)))
        path_4.add_point(Point(4, Coordinate(50.07005, 19.90359)))
        path_4.add_point(Point(4, Coordinate(50.07000, 19.90387)))
        path_4.add_point(Point(4, Coordinate(50.06995, 19.90417)))
        path_4.add_point(Point(4, Coordinate(50.06992, 19.90445)))
        path_4.add_point(Point(4, Coordinate(50.06988, 19.90478)))

        path_5 = Path()
        path_5.add_point(Point(5, Coordinate(50.06994, 19.90499)))
        path_5.add_point(Point(5, Coordinate(50.06998, 19.90480)))
        path_5.add_point(Point(5, Coordinate(50.07004, 19.90439)))
        path_5.add_point(Point(5, Coordinate(50.07009, 19.90408)))
        path_5.add_point(Point(5, Coordinate(50.07015, 19.90373)))
        path_5.add_point(Point(5, Coordinate(50.07019, 19.90343)))

        path_6 = Path()
        path_6.add_point(Point(6, Coordinate(50.06988, 19.90529)))
        path_6.add_point(Point(6, Coordinate(50.06996, 19.90491)))
        path_6.add_point(Point(6, Coordinate(50.07003, 19.90450)))
        path_6.add_point(Point(6, Coordinate(50.07008, 19.90417)))
        path_6.add_point(Point(6, Coordinate(50.07017, 19.90410)))
        path_6.add_point(Point(6, Coordinate(50.07041, 19.90420)))
        path_6.add_point(Point(6, Coordinate(50.07059, 19.90427)))

        self.algorithm.process([path_1, path_2, path_3, path_4, path_5, path_6])
