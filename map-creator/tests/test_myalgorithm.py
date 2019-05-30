import unittest

from map_creator.algorithm import MyAlgorithm
from map_creator.model import Coordinate, Egress, Ingress, Path, Point
from tests import NoLoggingTestCase


class MyAlgorithmTest(NoLoggingTestCase):
    def setUp(self):
        self.ref_point = Coordinate(44.51001, 7.24272)
        self.diff_distance = 0.1
        self.diff_heading = 2
        self.algorithm = MyAlgorithm(self.ref_point,
                                     self.diff_distance,
                                     self.diff_heading)

    def test_average_distance(self):
        threshold = 0.001   # 0.001 km = 1 m

        path1 = Path()

        path1.add_point(Point(1, Coordinate(45.83631, 4.75721)))
        path1.add_point(Point(1, Coordinate(45.83690, 4.75671)))
        path1.add_point(Point(1, Coordinate(45.83741, 4.75622)))

        path2 = Path()

        path2.add_point(Point(2, Coordinate(45.83639, 4.75731)))
        path2.add_point(Point(2, Coordinate(45.83703, 4.75694)))
        path2.add_point(Point(2, Coordinate(45.83764, 4.75675)))

        avg_distance = self.algorithm._average_distance(path1, path2)

        self.assertLessEqual(abs(avg_distance - 0.076113), threshold)

    def test_average_heading(self):
        threshold = 0.1     # 0.1 deg

        path = Path()

        path.add_point(Point(1, Coordinate(41.83972, 1.98145)))
        path.add_point(Point(1, Coordinate(41.84145, 1.98235)))
        path.add_point(Point(1, Coordinate(41.84341, 1.98276)))
        path.add_point(Point(1, Coordinate(41.84541, 1.98264)))
        path.add_point(Point(1, Coordinate(41.84723, 1.98230)))
        path.add_point(Point(1, Coordinate(41.84892, 1.98201)))
        path.add_point(Point(1, Coordinate(41.85064, 1.98210)))

        avg_heading = self.algorithm._average_heading(path)

        self.assertLessEqual(abs(avg_heading - 156.67718), threshold)

    def test_is_mergeable(self):
        path1 = Path()
        path2 = Path()
        path3 = Path()

        path1.add_point(Point(1, Coordinate(43.29468, 11.76338)))
        path1.add_point(Point(1, Coordinate(43.29518, 11.76334)))
        path1.add_point(Point(1, Coordinate(43.29550, 11.76332)))
        path1.add_point(Point(1, Coordinate(43.29601, 11.76327)))

        path2.add_point(Point(2, Coordinate(43.29524, 11.76321)))
        path2.add_point(Point(2, Coordinate(43.29557, 11.76318)))
        path2.add_point(Point(2, Coordinate(43.29596, 11.76316)))
        path2.add_point(Point(2, Coordinate(43.29658, 11.76313)))

        path3.add_point(Point(1, Coordinate(43.29550, 11.76331)))
        path3.add_point(Point(1, Coordinate(43.29579, 11.76328)))
        path3.add_point(Point(1, Coordinate(43.29596, 11.76346)))
        path3.add_point(Point(1, Coordinate(43.29612, 11.76378)))

        self.assertTrue(self.algorithm._is_mergeable(path1, path2))

        self.assertFalse(self.algorithm._is_mergeable(path2, path3))

    def test_merge_path(self):
        path1 = Path()
        path2 = Path()

        path1.add_point(Point(1, Coordinate(43.29468, 11.76338)))
        path1.add_point(Point(1, Coordinate(43.29518, 11.76334)))
        path1.add_point(Point(1, Coordinate(43.29550, 11.76332)))
        path1.add_point(Point(1, Coordinate(43.29601, 11.76327)))

        path2.add_point(Point(2, Coordinate(43.29524, 11.76321)))
        path2.add_point(Point(2, Coordinate(43.29557, 11.76318)))
        path2.add_point(Point(2, Coordinate(43.29596, 11.76316)))
        path2.add_point(Point(2, Coordinate(43.29658, 11.76313)))

        path1, path2 = self.algorithm._merge(path1, path2)

        self.assertEqual(len(path1.points), 4)

        self.assertIsNone(path2)

    def test_merge_egress(self):
        egress1 = Egress()
        egress2 = Egress()

        egress1.add_point(Point(1, Coordinate(43.29468, 11.76338)))
        egress1.add_point(Point(1, Coordinate(43.29518, 11.76334)))
        egress1.add_point(Point(1, Coordinate(43.29550, 11.76332)))
        egress1.add_point(Point(1, Coordinate(43.29601, 11.76327)))

        egress2.add_point(Point(2, Coordinate(43.29524, 11.76321)))
        egress2.add_point(Point(2, Coordinate(43.29557, 11.76318)))
        egress2.add_point(Point(2, Coordinate(43.29596, 11.76316)))
        egress2.add_point(Point(2, Coordinate(43.29658, 11.76313)))

        egress1, egress2 = self.algorithm._merge(egress1, egress2)

        self.assertEqual(len(egress1.points), 4)

        self.assertIsNone(egress2)

    def test_merge_ingress(self):
        ingress1 = Ingress()
        ingress2 = Ingress()

        ingress1.add_point(Point(1, Coordinate(43.29468, 11.76338)))
        ingress1.add_point(Point(1, Coordinate(43.29518, 11.76334)))
        ingress1.add_point(Point(1, Coordinate(43.29550, 11.76332)))
        ingress1.add_point(Point(1, Coordinate(43.29601, 11.76327)))

        ingress2.add_point(Point(2, Coordinate(43.29524, 11.76321)))
        ingress2.add_point(Point(2, Coordinate(43.29557, 11.76318)))
        ingress2.add_point(Point(2, Coordinate(43.29596, 11.76316)))
        ingress2.add_point(Point(2, Coordinate(43.29658, 11.76313)))

        egress1 = Egress()
        egress2 = Egress()

        egress1.add_point(Point(1, Coordinate(44, 12)))
        egress2.add_point(Point(2, Coordinate(45, 13)))

        ingress1.add_egress(egress1)
        ingress2.add_egress(egress2)

        ingress1, ingress2 = self.algorithm._merge(ingress1, ingress2)

        self.assertEqual(len(ingress1.points), 4)
        self.assertEqual(ingress1.egresses, [egress1, egress2])

        self.assertIsNone(ingress2)

    # TODO: fix unittest
    @unittest.skip
    def test_process(self):
        threshold = 0.005   # 0.005 deg

        self.algorithm._ref_point = Coordinate(47.05889, 15.44551)

        path1 = Path()
        path2 = Path()
        path3 = Path()
        path4 = Path()

        path1.add_point(Point(1, Coordinate(47.05865, 15.44394)))
        path1.add_point(Point(1, Coordinate(47.05870, 15.44439)))
        path1.add_point(Point(1, Coordinate(47.05878, 15.44517)))
        path1.add_point(Point(1, Coordinate(47.05888, 15.44551)))
        path1.add_point(Point(1, Coordinate(47.05913, 15.44636)))

        path2.add_point(Point(2, Coordinate(47.05867, 15.44394)))
        path2.add_point(Point(2, Coordinate(47.05870, 15.44440)))
        path2.add_point(Point(2, Coordinate(47.05876, 15.44507)))
        path2.add_point(Point(2, Coordinate(47.05887, 15.44550)))
        path2.add_point(Point(2, Coordinate(47.05844, 15.44574)))

        path3.add_point(Point(3, Coordinate(47.05912, 15.44637)))
        path3.add_point(Point(3, Coordinate(47.05897, 15.44585)))
        path3.add_point(Point(3, Coordinate(47.05890, 15.44544)))
        path3.add_point(Point(3, Coordinate(47.05886, 15.44489)))
        path3.add_point(Point(3, Coordinate(47.05877, 15.44408)))

        path4.add_point(Point(4, Coordinate(47.05912, 15.44637)))
        path4.add_point(Point(4, Coordinate(47.05897, 15.44585)))
        path4.add_point(Point(4, Coordinate(47.05890, 15.44544)))
        path4.add_point(Point(4, Coordinate(47.05886, 15.44489)))
        path4.add_point(Point(4, Coordinate(47.05877, 15.44408)))

        map_data = self.algorithm.process([path1, path2, path3, path4])

        self.assertEqual(len(map_data.ingresses), 2)

        self.assertEqual(len(map_data.ingresses[0].points), 6)
        self.assertEqual(len(map_data.ingresses[1].points), 6)

        self.assertEqual(
            map_data.ingresses[0].points[0].position.latitude, path2.points[0].position.latitude)
        self.assertEqual(
            map_data.ingresses[0].points[0].position.longitude, path2.points[0].position.longitude)
        self.assertLessEqual(abs(
            map_data.ingresses[0].points[0].heading - path2.points[0].heading), threshold)

        self.assertEqual(
            map_data.ingresses[0].points[1].position.latitude, path2.points[1].position.latitude)
        self.assertEqual(
            map_data.ingresses[0].points[1].position.longitude, path2.points[1].position.longitude)
        self.assertLessEqual(abs(
            map_data.ingresses[0].points[1].heading - path2.points[1].heading), threshold)

        self.assertEqual(
            map_data.ingresses[0].points[2].position.latitude, path2.points[2].position.latitude)
        self.assertEqual(
            map_data.ingresses[0].points[2].position.longitude, path2.points[2].position.longitude)
        self.assertLessEqual(abs(
            map_data.ingresses[0].points[2].heading - path2.points[2].heading), threshold)

        self.assertEqual(
            map_data.ingresses[0].points[3].position.latitude, path2.points[3].position.latitude)
        self.assertEqual(
            map_data.ingresses[0].points[3].position.longitude, path2.points[3].position.longitude)
        self.assertLessEqual(abs(
            map_data.ingresses[0].points[3].heading - path2.points[3].heading), threshold)

        self.assertEqual(
            map_data.ingresses[1].points[0].position.latitude, path3.points[0].position.latitude)
        self.assertEqual(
            map_data.ingresses[1].points[0].position.longitude, path3.points[0].position.longitude)
        self.assertLessEqual(abs(
            map_data.ingresses[1].points[0].heading - path3.points[0].heading), threshold)

        self.assertEqual(
            map_data.ingresses[1].points[1].position.latitude, path3.points[1].position.latitude)
        self.assertEqual(
            map_data.ingresses[1].points[1].position.longitude, path3.points[1].position.longitude)
        self.assertLessEqual(abs(
            map_data.ingresses[1].points[1].heading - path3.points[1].heading), threshold)

        self.assertEqual(
            map_data.ingresses[1].points[2].position.latitude, path3.points[2].position.latitude)
        self.assertEqual(
            map_data.ingresses[1].points[2].position.longitude, path3.points[2].position.longitude)
        self.assertLessEqual(abs(
            map_data.ingresses[1].points[2].heading - path3.points[2].heading), threshold)

        self.assertEqual(len(map_data.ingresses[0].egresses), 2)
        self.assertEqual(len(map_data.ingresses[1].egresses), 1)

        self.assertEqual(len(map_data.ingresses[0].egresses[0].points), 6)
        self.assertEqual(len(map_data.ingresses[0].egresses[1].points), 6)
        self.assertEqual(len(map_data.ingresses[1].egresses[0].points), 6)

        self.assertEqual(
            map_data.ingresses[0].egresses[0].points[0].position.latitude, path2.points[4].position.latitude)
        self.assertEqual(
            map_data.ingresses[0].egresses[0].points[0].position.longitude, path2.points[4].position.longitude)
        self.assertLessEqual(abs(
            map_data.ingresses[0].egresses[0].points[0].heading, path2.points[4].heading), threshold)

        self.assertEqual(
            map_data.ingresses[0].egresses[1].points[0].position.latitude, path1.points[4].position.latitude)
        self.assertEqual(
            map_data.ingresses[0].egresses[1].points[0].position.longitude, path1.points[4].position.longitude)
        self.assertLessEqual(abs(
            map_data.ingresses[0].egresses[1].points[0].heading, path1.points[4].heading), threshold)

        self.assertEqual(
            map_data.ingresses[1].egresses[0].points[0].position.latitude, path3.points[3].position.latitude)
        self.assertEqual(
            map_data.ingresses[1].egresses[0].points[0].position.longitude, path3.points[3].position.longitude)
        self.assertLessEqual(abs(
            map_data.ingresses[1].egresses[0].points[0].heading, path3.points[3].heading), threshold)
