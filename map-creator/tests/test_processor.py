from map_creator.model import Coordinate, Path, Point
from map_creator.processor import Preprocessor

from tests import NoLoggingTestCase


class PreprocessorTest(NoLoggingTestCase):
    def setUp(self):
        ref_point = Coordinate(44.51001, 7.24272)
        range_ = 0.015
        num_points = 10
        self.preprocessor = Preprocessor(ref_point, range_, num_points)

    def test_filter_points(self):
        points = [
            Point(1, Coordinate(44.51012, 7.24281)),
            Point(1, Coordinate(44.51023, 7.24250)),
            Point(1, Coordinate(44.51000, 7.24278)),
            Point(1, Coordinate(44.50992, 7.24271)),
            Point(1, Coordinate(44.51001, 7.24264)),
            Point(1, Coordinate(44.51051, 7.24281)),
            Point(1, Coordinate(44.51018, 7.24239)),
            Point(1, Coordinate(44.50985, 7.24254))
        ]

        filtered = self.preprocessor.filter_points(points)

        self.assertEqual(filtered, [
            Point(1, Coordinate(44.51012, 7.24281)),
            Point(1, Coordinate(44.51000, 7.24278)),
            Point(1, Coordinate(44.50992, 7.24271)),
            Point(1, Coordinate(44.51001, 7.24264))
        ])