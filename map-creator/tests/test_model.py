import json

from map_creator.model import Coordinate, Egress, Ingress, Map, ModelJSONEncoder, ModelJSONDecoder, Path, Point
from tests import NoLoggingTestCase


class CoordinateTest(NoLoggingTestCase):
    def test_distance(self):
        threshold = 0.001   # 0.001 km = 1 m
        c1 = Coordinate(47.47085, 19.05291)
        c2 = Coordinate(47.47312, 19.06369)
        self.assertLessEqual(abs(c1.distance(c2) - 0.84866), threshold)

        threshold = 0.02   # 0.02 km = 20 m
        c1 = Coordinate(53.404, -2.966)
        c2 = Coordinate(53.462, -2.250)
        self.assertLessEqual(abs(c1.distance(c2) - 47.87), threshold)

    def test_heading(self):
        threshold = 0.1   # 0.1 deg
        c1 = Coordinate(47.47085, 19.05291)
        c2 = Coordinate(47.47126749, 19.05315656)
        self.assertLessEqual(abs(c1.heading(c2) - 21.823), threshold)

        threshold = 1   # 1 deg
        c1 = Coordinate(53.404, -2.966)
        c2 = Coordinate(53.39982678, -2.66178226)
        self.assertLessEqual(abs(c1.heading(c2) - 91.19281), threshold)

    def test_create_at(self):
        threshold = 0.001    # 0.001 deg

        c1 = Coordinate(1.234, 56.789)
        distance = 1.234
        heading = 56.789

        c2 = c1.create_at(distance, heading)

        self.assertLessEqual(abs(c2.latitude - 1.24011251), threshold)
        self.assertLessEqual(abs(c2.longitude - 56.7982767), threshold)

    def test_to_json(self):
        expected = r'{"mc_model": "Coordinate", "latitude": 10, "longitude": 20}'

        c = Coordinate(10, 20)
        json_str = json.dumps(c.to_json())

        self.assertEqual(json_str, expected)

        json_str = json.dumps(c, cls=ModelJSONEncoder)

        self.assertEqual(json_str, expected)

    def test_from_json(self):
        expected = Coordinate(10, 20)

        json_obj = {'mc_model': 'Coordinate', 'latitude': 10, 'longitude': 20}
        json_str = json.dumps(json_obj)

        c = Coordinate.from_json(json_obj)

        self.assertEqual(c, expected)

        c = json.loads(json_str, cls=ModelJSONDecoder)

        self.assertEqual(c, expected)


class PointTest(NoLoggingTestCase):
    def test_to_json(self):
        expected = r'{"mc_model": "Point", "id": 1, "position": ' \
            + r'{"mc_model": "Coordinate", "latitude": 10, "longitude": 20}, "heading": 0}'

        p = Point(1, Coordinate(10, 20))
        json_str = json.dumps(p.to_json())

        self.assertEqual(json_str, expected)

        json_str = json.dumps(p, cls=ModelJSONEncoder)

        self.assertEqual(json_str, expected)

    def test_from_json(self):
        expected = Point(1, Coordinate(10, 20))

        json_obj = {'mc_model': 'Point', 'id': 1, 'position': {
            'mc_model': 'Coordinate', 'latitude': 10, 'longitude': 20}, 'heading': 0}
        json_str = json.dumps(json_obj)

        p = Point.from_json(json_obj)

        self.assertEqual(p, expected)

        p = json.loads(json_str, cls=ModelJSONDecoder)

        self.assertEqual(p, expected)


class PathTest(NoLoggingTestCase):
    def test_add_point(self):
        path = Path()

        c1 = Coordinate(10, 20)
        p1 = Point(10, c1)
        path.add_point(p1)
        self.assertEqual(len(path.points), 1)

        c2 = Coordinate(21, 21)
        p2 = Point(10, c2)
        path.add_point(p2)
        self.assertEqual(len(path.points), 2)

        c3 = Coordinate(42, 32)
        p3 = Point(20, c3)
        path.add_point(p3)
        self.assertEqual(len(path.points), 2)

    def test_length(self):
        threshold = 0.001   # 0.001 km = 1 m

        path = Path()

        path.add_point(Point(1, Coordinate(46.99988, 7.69637)))
        path.add_point(Point(1, Coordinate(46.99901, 7.69794)))
        path.add_point(Point(1, Coordinate(46.99846, 7.69907)))
        path.add_point(Point(1, Coordinate(46.99819, 7.70072)))

        length = path.length()

        self.assertLessEqual(abs(length - 0.38737), threshold)

    def test_to_json(self):
        expected = r'{"mc_model": "Path", "id": 1, "points": ['\
            + r'{"mc_model": "Point", "id": 1, "position": ' \
            + r'{"mc_model": "Coordinate", "latitude": 10, "longitude": 20}, "heading": 0}]}'

        p = Path()
        p.add_point(Point(1, Coordinate(10, 20)))
        json_str = json.dumps(p.to_json())

        self.assertEqual(json_str, expected)

        json_str = json.dumps(p, cls=ModelJSONEncoder)

        self.assertEqual(json_str, expected)

    def test_from_json(self):
        expected = Path()
        expected.add_point(Point(1, Coordinate(10, 20)))

        json_obj = {'mc_model': 'Path', 'id': 1, 'points': [{
            'mc_model': 'Point', 'id': 1, 'position': {
                'mc_model': 'Coordinate', 'latitude': 10, 'longitude': 20}, 'heading': 0}]}
        json_str = json.dumps(json_obj)

        p = Path.from_json(json_obj)

        self.assertEqual(p, expected)

        p = json.loads(json_str, cls=ModelJSONDecoder)

        self.assertEqual(p, expected)


class EgressTest(NoLoggingTestCase):
    def test_to_json(self):
        expected = r'{"mc_model": "Egress", "id": 1, "points": ['\
            + r'{"mc_model": "Point", "id": 1, "position": ' \
            + r'{"mc_model": "Coordinate", "latitude": 10, "longitude": 20}, "heading": 0}]}'

        e = Egress()
        e.add_point(Point(1, Coordinate(10, 20)))
        json_str = json.dumps(e.to_json())

        self.assertEqual(json_str, expected)

        json_str = json.dumps(e, cls=ModelJSONEncoder)

        self.assertEqual(json_str, expected)

    def test_from_json(self):
        expected = Egress()
        expected.add_point(Point(1, Coordinate(10, 20)))

        json_obj = {'mc_model': 'Egress', 'id': 1, 'points': [{
            'mc_model': 'Point', 'id': 1, 'position': {
                'mc_model': 'Coordinate', 'latitude': 10, 'longitude': 20}, 'heading': 0}]}
        json_str = json.dumps(json_obj)

        e = Egress.from_json(json_obj)

        self.assertEqual(e, expected)

        e = json.loads(json_str, cls=ModelJSONDecoder)

        self.assertEqual(e, expected)


class IngressTest(NoLoggingTestCase):
    def test_to_json(self):
        expected = r'{"mc_model": "Ingress", "id": 1, "points": [' \
            + r'{"mc_model": "Point", "id": 1, "position": ' \
            + r'{"mc_model": "Coordinate", "latitude": 10, "longitude": 20}, ' \
            + r'"heading": 0}], "egresses": [' \
            + r'{"mc_model": "Egress", "id": 1, "points": [' \
            + r'{"mc_model": "Point", "id": 1, "position": ' \
            + r'{"mc_model": "Coordinate", "latitude": 10, "longitude": 20}, ' \
            + r'"heading": 0}]}]}'

        i = Ingress()
        i.add_point(Point(1, Coordinate(10, 20)))
        e = Egress()
        e.add_point(Point(1, Coordinate(10, 20)))
        i.add_egress(e)

        json_str = json.dumps(i.to_json())

        self.assertEqual(json_str, expected)

        json_str = json.dumps(i, cls=ModelJSONEncoder)

        self.assertEqual(json_str, expected)

    def test_from_json(self):
        expected = Ingress()
        expected.add_point(Point(1, Coordinate(10, 20)))
        e = Egress()
        e.add_point(Point(1, Coordinate(10, 20)))
        expected.add_egress(e)

        json_obj = {'mc_model': 'Ingress', 'id': 1, 'points': [
            {'mc_model': 'Point', 'id': 1, 'position':
             {'mc_model': 'Coordinate', 'latitude': 10, 'longitude': 20},
             'heading': 0}], 'egresses': [
                 {'mc_model': 'Egress', 'id': 1, 'points': [
                     {'mc_model': 'Point', 'id': 1, 'position':
                      {'mc_model': 'Coordinate', 'latitude': 10, 'longitude': 20},
                      'heading': 0}]}]}
        json_str = json.dumps(json_obj)

        i = Ingress.from_json(json_obj)

        self.assertEqual(i, expected)

        i = json.loads(json_str, cls=ModelJSONDecoder)

        self.assertEqual(i, expected)


class MapTest(NoLoggingTestCase):
    def test_to_json(self):
        expected = r'{"mc_model": "Map", "ref_point": {"mc_model": "Coordinate", "latitude": 10, ' \
            + r'"longitude": 20}, "ingresses": ' \
            + r'[{"mc_model": "Ingress", "id": 1, "points": [' \
            + r'{"mc_model": "Point", "id": 1, "position": ' \
            + r'{"mc_model": "Coordinate", "latitude": 10, "longitude": 20}, ' \
            + r'"heading": 0}], "egresses": [' \
            + r'{"mc_model": "Egress", "id": 1, "points": [' \
            + r'{"mc_model": "Point", "id": 1, "position": ' \
            + r'{"mc_model": "Coordinate", "latitude": 10, "longitude": 20}, ' \
            + r'"heading": 0}]}]}]}'

        i = Ingress()
        i.add_point(Point(1, Coordinate(10, 20)))
        e = Egress()
        e.add_point(Point(1, Coordinate(10, 20)))
        i.add_egress(e)
        m = Map(Coordinate(10, 20), [i, ])

        json_str = json.dumps(m.to_json())

        self.assertEqual(json_str, expected)

        json_str = json.dumps(m, cls=ModelJSONEncoder)

        self.assertEqual(json_str, expected)

    def test_from_json(self):
        i = Ingress()
        i.add_point(Point(1, Coordinate(10, 20)))
        e = Egress()
        e.add_point(Point(1, Coordinate(10, 20)))
        i.add_egress(e)
        expected = Map(Coordinate(10, 20), [i, ])

        json_obj = {'mc_model': 'Map', 'ref_point': {'mc_model': 'Coordinate', 'latitude': 10, 'longitude': 20},
                    'ingresses': [{'mc_model': 'Ingress', 'id': 1, 'points': [
                        {'mc_model': 'Point', 'id': 1, 'position':
                         {'mc_model': 'Coordinate', 'latitude': 10, 'longitude': 20},
                         'heading': 0}], 'egresses': [
                             {'mc_model': 'Egress', 'id': 1, 'points': [
                                 {'mc_model': 'Point', 'id': 1, 'position':
                                  {'mc_model': 'Coordinate',
                                   'latitude': 10, 'longitude': 20},
                                  'heading': 0}]}]}]}
        json_str = json.dumps(json_obj)

        m = Map.from_json(json_obj)

        self.assertEqual(m, expected)

        m = json.loads(json_str, cls=ModelJSONDecoder)

        self.assertEqual(m, expected)
