from tests import NoLoggingTestCase
from map_creator.model import Coordinate, Path, Point
from map_creator.utils import closest_point, combine_paths, condense, find_key_points


class UtilsTest(NoLoggingTestCase):
    # def test_adjust(self):
    #     path_1 = Path()
    #     path_2 = Path()

    #     path_1.add_point(Point(1, Coordinate(47.56463, 19.04890)))
    #     path_1.add_point(Point(1, Coordinate(47.56615, 19.04938)))
    #     path_1.add_point(Point(1, Coordinate(47.56685, 19.04945)))
    #     path_1.add_point(Point(1, Coordinate(47.56774, 19.04914)))


    #     path_2.add_point(Point(2, Coordinate(47.56870, 19.04847)))
    #     path_2.add_point(Point(2, Coordinate(47.56792, 19.04880)))
    #     path_2.add_point(Point(2, Coordinate(47.56735, 19.04907)))
    #     path_2.add_point(Point(2, Coordinate(47.56677, 19.04922)))
    #     path_2.add_point(Point(2, Coordinate(47.56603, 19.04911)))
    #     path_2.add_point(Point(2, Coordinate(47.56446, 19.04847)))

    #     adj_path_1, adj_path_2 = adjust(path_1, path_2)

    #     print('path_1')
    #     for point in path_1.points:
    #         print(point.position.latitude, point.position.longitude)

    #     print('path_2')
    #     for point in path_2.points:
    #         print(point.position.latitude, point.position.longitude)

    #     print('adj_path_1')
    #     for point in adj_path_1.points:
    #         print(point.position.latitude, point.position.longitude)

    #     print('adj_path_2')
    #     for point in adj_path_2.points:
    #         print(point.position.latitude, point.position.longitude)

    def test_condense(self):
        path = Path()

        path.add_point(Point(1, Coordinate(47.56463, 19.04890)))
        path.add_point(Point(1, Coordinate(47.56615, 19.04938)))
        path.add_point(Point(1, Coordinate(47.56685, 19.04945)))
        path.add_point(Point(1, Coordinate(47.56774, 19.04914)))

        condensed = condense(path, 50)

        self.assertEqual(len(condensed.points), 50)

        key_points_path = find_key_points(path)
        key_points_condensed = find_key_points(condensed)

        self.assertTrue(all(key_point in key_points_condensed for key_point in key_points_path))

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
