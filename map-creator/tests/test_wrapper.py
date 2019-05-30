from tests import NoLoggingTestCase
from map_creator.model import Coordinate, Egress, Ingress, Map, Path, Point
from map_creator.wrapper import WrappedCoordinate, WrappedEgress, WrappedIngress, WrappedMap, WrappedPath, WrappedPoint


class WrappedCoordinateTest(NoLoggingTestCase):
    def setUp(self):
        self.coordinate = Coordinate(10, 20)

    def test_to_json(self):
        wrapped_coordinate = WrappedCoordinate(self.coordinate)
        expected = {'latitude': 10, 'longitude': 20}
        self.assertEqual(wrapped_coordinate.to_json(), expected)

    def test_from_json(self):
        obj = self.coordinate.to_json()
        wrapped_coordinate = WrappedCoordinate.from_json(obj)
        self.assertEqual(self.coordinate, wrapped_coordinate.obj)


class WrappedPointTest(NoLoggingTestCase):
    def setUp(self):
        self.point = Point(1, Coordinate(10, 20))

    def test_to_json(self):
        wrapped_point = WrappedPoint(self.point)
        expected = {'latitude': 10, 'longitude': 20}
        self.assertEqual(wrapped_point.to_json(), expected)

    def test_from_json(self):
        obj = self.point.to_json()
        wrapped_point = WrappedPoint.from_json(obj)
        self.assertEqual(self.point, wrapped_point.obj)


class WrappedPathTest(NoLoggingTestCase):
    def setUp(self):
        self.path = Path()
        self.path.add_point(Point(1, Coordinate(10, 20)))

    def test_to_json(self):
        wrapped_path = WrappedPath(self.path)
        expected = [{'latitude': 10, 'longitude': 20}]
        self.assertEqual(wrapped_path.to_json(), expected)

    def test_from_json(self):
        obj = self.path.to_json()
        wrapped_path = WrappedPath.from_json(obj)
        self.assertEqual(self.path, wrapped_path.obj)


class WrappedEgressTest(NoLoggingTestCase):
    def setUp(self):
        self.egress = Egress()
        self.egress.add_point(Point(1, Coordinate(10, 20)))

    def test_to_json(self):
        wrapped_egress = WrappedEgress(self.egress)
        expected = [{'latitude': 10, 'longitude': 20}]
        self.assertEqual(wrapped_egress.to_json(), expected)

    def test_from_json(self):
        obj = self.egress.to_json()
        wrapped_egress = WrappedEgress.from_json(obj)
        self.assertEqual(self.egress, wrapped_egress.obj)


class WrappedIngressTest(NoLoggingTestCase):
    def setUp(self):
        self.ingress = Ingress()
        self.ingress.add_point(Point(1, Coordinate(10, 20)))
        egress = Egress()
        egress.add_point(Point(1, Coordinate(10, 20)))
        self.ingress.add_egress(egress)

    def test_to_json(self):
        wrapped_ingress = WrappedIngress(self.ingress)
        expected = {
            'points': [{'latitude': 10, 'longitude': 20}],
            'egresses': [
                [{'latitude': 10, 'longitude': 20}]
            ]
        }
        self.assertEqual(wrapped_ingress.to_json(), expected)

    def test_to_json_without_egress(self):
        self.ingress.egresses = []
        wrapped_ingress = WrappedIngress(self.ingress)
        expected = {
            'points': [{'latitude': 10, 'longitude': 20}],
            'egresses': []
        }
        self.assertEqual(wrapped_ingress.to_json(), expected)

    def test_from_json(self):
        obj = self.ingress.to_json()
        wrapped_ingress = WrappedIngress.from_json(obj)
        self.assertEqual(self.ingress, wrapped_ingress.obj)


class WrappedMapTest(NoLoggingTestCase):
    def setUp(self):
        ingress = Ingress()
        ingress.add_point(Point(1, Coordinate(10, 20)))
        egress = Egress()
        egress.add_point(Point(1, Coordinate(10, 20)))
        ingress.add_egress(egress)
        self.map_data = Map(Coordinate(10, 20), [ingress, ])

    def test_to_json(self):
        wrapped_map = WrappedMap(self.map_data)
        expected = {
            'ref_point': {'latitude': 10, 'longitude': 20},
            'ingresses': [{
                'points': [{'latitude': 10, 'longitude': 20}],
                'egresses': [
                    [{'latitude': 10, 'longitude': 20}]
                ]
            }]
        }
        self.assertEqual(wrapped_map.to_json(), expected)

    def test_to_json_without_egress(self):
        self.map_data.ingresses[0].egresses = []
        wrapped_map = WrappedMap(self.map_data)
        expected = {
            'ref_point': {'latitude': 10, 'longitude': 20},
            'ingresses': [{
                'points': [{'latitude': 10, 'longitude': 20}],
                'egresses': []
            }]
        }
        self.assertEqual(wrapped_map.to_json(), expected)

    def test_from_json(self):
        obj = self.map_data.to_json()
        wrapped_map = WrappedMap.from_json(obj)
        self.assertEqual(self.map_data, wrapped_map.obj)
