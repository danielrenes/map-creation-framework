from tests import NoLoggingTestCase
from map_creator.model import Coordinate, Path, Point
from map_creator.utils import closest_point, combine_paths, interpolate


class UtilsTest(NoLoggingTestCase):
    def test_closest_point(self):
        target = Point(None, Coordinate(47.49816, 19.04051))
        point_1 = Point(None, Coordinate(47.49826, 19.04072))
        point_2 = Point(None, Coordinate(47.49853, 19.04061))
        point_3 = Point(None, Coordinate(47.49851, 19.04017))
        point_4 = Point(None, Coordinate(47.49820, 19.03952))
        point_5 = Point(None, Coordinate(47.49764, 19.04076))

        closest = closest_point(target, [point_1, point_2,
                                         point_3, point_4, point_5])

        self.assertEqual(closest, point_1)

    def test_interpolate(self):
        path = Path()

        path.add_point(Point(1, Coordinate(44.51012, 7.24281)))
        path.add_point(Point(1, Coordinate(44.50992, 7.24271)))
        path.add_point(Point(1, Coordinate(44.51001, 7.24264)))
        path.add_point(Point(1, Coordinate(44.51018, 7.24239)))

        distance = path.length() / 10
        threshold = distance / 5

        interpolated = interpolate(path, 10)

        self.assertEqual(len(interpolated.points), 10)
        self.assertEqual(interpolated.points[0], path.points[0])
        self.assertEqual(interpolated.points[-1], path.points[-1])

        for i in range(len(interpolated.points) - 1):
            c1 = interpolated.points[i].position
            c2 = interpolated.points[i + 1].position
            self.assertLessEqual(abs(c1.distance(c2) - distance), threshold)

    def test_combine_paths(self):
        path_1 = Path()
        path_1.add_point(Point(1, Coordinate(50.08313, 14.41323)))
        path_1.add_point(Point(1, Coordinate(50.08321, 14.41325)))
        path_1.add_point(Point(1, Coordinate(50.08330, 14.41326)))
        path_1.add_point(Point(1, Coordinate(50.08337, 14.41325)))
        path_1.add_point(Point(1, Coordinate(50.08345, 14.41330)))
        path_1.add_point(Point(1, Coordinate(50.08354, 14.41329)))

        path_2 = Path()
        path_2.add_point(Point(2, Coordinate(50.08300, 14.41321)))
        path_2.add_point(Point(2, Coordinate(50.08326, 14.41326)))
        path_2.add_point(Point(2, Coordinate(50.08346, 14.41328)))
        path_2.add_point(Point(2, Coordinate(50.08376, 14.41334)))

        combined = combine_paths([path_1, path_2])

        self.assertEqual(combined.id_, path_1.id_)
        self.assertLessEqual(len(combined.points),
                             len(path_1.points) + len(path_2.points))
