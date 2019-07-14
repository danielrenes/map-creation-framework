import time

from map_creator.model import Coordinate, Path, Point
from map_creator.processor import Preprocessor, Processor
from map_creator.rsu import Rsu

from tests import NoLoggingTestCase


class RsuTest(NoLoggingTestCase):
    def test_update_paths(self):
        ref_point = Coordinate(0, 0)
        preprocessor = Preprocessor(ref_point=ref_point,
                                    range_=1,
                                    num_of_points=10)
        processor = Processor(algorithm=None,
                              preprocessor=preprocessor)
        rsu = Rsu(processor=processor,
                  time_window_seconds=0.2)

        path = Path()
        point_1 = Point(1, Coordinate(11, 11))
        point_2 = Point(1, Coordinate(12, 12))

        path.add_point(point_1)
        path.add_point(point_2)

        rsu.add_path(path)

        self.assertEqual(len(rsu.paths), 1)
        self.assertEqual(len(rsu.paths[0].points), 2)

        time.sleep(0.1)

        point_3 = Point(1, Coordinate(13, 13))
        rsu.add_point(0, point_3)

        time.sleep(0.1)

        rsu._update_paths()

        self.assertEqual(len(rsu.paths), 1)
        self.assertEqual(len(rsu.paths[0].points), 1)
        self.assertEqual(rsu.paths[0].points[0], point_3)

        time.sleep(0.2)

        rsu._update_paths()

        self.assertEqual(len(rsu.paths), 0)
