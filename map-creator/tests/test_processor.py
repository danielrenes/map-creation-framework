from map_creator.model import Coordinate, Egress, Ingress, Map, Path, Point
from map_creator.processor import Preprocessor, Processor

from tests import NoLoggingTestCase


class PreprocessorTest(NoLoggingTestCase):
    def setUp(self):
        ref_point = Coordinate(44.51001, 7.24272)
        range_ = 0.015
        num_points = 10
        self.preprocessor = Preprocessor(ref_point, range_, num_points)
        self.processor = Processor(None, None)

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

    def test_postprocess(self):
        ref_point = Coordinate(47.48024, 19.03635)

        ingress_11 = Ingress()
        ingress_11.add_point(Point(1, Coordinate(47.48068, 19.03508)))
        ingress_11.add_point(Point(1, Coordinate(47.48048, 19.03561)))
        ingress_11.add_point(Point(1, Coordinate(47.48020, 19.03624)))

        egress_111 = Egress()
        egress_111.add_point(Point(2, Coordinate(47.48014, 19.03638)))
        egress_111.add_point(Point(2, Coordinate(47.47994, 19.03684)))

        egress_112 = Egress()
        egress_112.add_point(Point(3, Coordinate(47.48011, 19.03620)))
        egress_112.add_point(Point(3, Coordinate(47.47990, 19.03602)))
        egress_112.add_point(Point(3, Coordinate(47.47953, 19.03575)))

        ingress_11.add_egress(egress_111)
        ingress_11.add_egress(egress_112)

        ingresses_1 = [ingress_11, ]

        ingress_21 = Ingress()
        ingress_21.add_point(Point(4, Coordinate(47.48072, 19.03506)))
        ingress_21.add_point(Point(4, Coordinate(47.48024, 19.03615)))

        egress_211 = Egress()
        egress_211.add_point(Point(5, Coordinate(47.48038, 19.03650)))
        egress_211.add_point(Point(5, Coordinate(47.48085, 19.03716)))

        egress_212 = Egress()
        egress_212.add_point(Point(6, Coordinate(47.48013, 19.03636)))
        egress_212.add_point(Point(6, Coordinate(47.47986, 19.03709)))

        ingress_21.add_egress(egress_211)
        ingress_21.add_egress(egress_212)

        ingress_22 = Ingress()
        ingress_22.add_point(Point(7, Coordinate(47.47985, 19.03757)))
        ingress_22.add_point(Point(7, Coordinate(47.48029, 19.03658)))

        egress_221 = Egress()
        egress_221.add_point(Point(8, Coordinate(47.48046, 19.03661)))
        egress_221.add_point(Point(8, Coordinate(47.48074, 19.03700)))

        ingress_22.add_egress(egress_221)

        ingresses_2 = [ingress_21, ingress_22]

        map_1 = Map(ref_point, ingresses_1)
        map_2 = Map(ref_point, ingresses_2)

        map_aggr = self.processor.postprocess(map_1, map_2)

        self.assertEqual(len(map_aggr.ingresses), 2)
        self.assertEqual(len(map_aggr.ingresses[0].egresses), 3)
        self.assertEqual(len(map_aggr.ingresses[1].egresses), 1)
