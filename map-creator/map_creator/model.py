from datetime import datetime
import json
from math import asin, atan2, cos, degrees, pi, radians, sin, sqrt
from typing import Any, List


class JsonSerializable:
    def __init__(self):
        self.mc_model = self.__class__.__name__

    def to_json(self):
        raise NotImplementedError

    @staticmethod
    def from_json(obj):
        raise NotImplementedError


def vector_pairs(x: 'Vector', y: 'Vector', permissive: bool):
    x_idx, y_idx = 0, 0
    x_max, y_max = len(x.data), len(y.data)

    reached_end_x, reached_end_y = x_idx >= x_max, y_idx >= y_max
    if not permissive:
        reached_end_x = True if reached_end_y else reached_end_x
        reached_end_y = True if reached_end_x else reached_end_y

    while not reached_end_x or not reached_end_y:
        yield (x[x_idx], y[y_idx])

        x_idx += 1
        y_idx += 1

        if x_idx >= x_max:
            if not permissive:
                reached_end_y = True
            reached_end_x = True
            x_idx = 0

        if y_idx >= y_max:
            if not permissive:
                reached_end_x = True
            reached_end_y = True
            y_idx = 0


class Vector:
    def __init__(self, data=None, is_permissive=False):
        self.data = data if data else []
        self.is_permissive = is_permissive
        self.iterator = 0

    def __len__(self) -> int:
        null_vector = Vector(data=[0 for _ in self.data])
        diff_vector = self - null_vector
        return int(sqrt(sum([item ** 2 for item in diff_vector.data])))

    def __eq__(self, other: 'Vector') -> bool:
        if not isinstance(other, Vector):
            return NotImplemented

        if len(self.data) != len(other.data):
            return False

        for xi, yi in zip(self.data, other.data):
            if xi != yi:
                return False

        return True

    def __ne__(self, other: 'Vector') -> bool:
        return not self.__eq__(other)

    def __iter__(self):
        self.iterator = 0
        return self

    def __next__(self):
        if self.iterator < len(self.data):
            item = self.data[self.iterator]
            self.iterator = self.iterator + 1
            return item
        else:
            raise StopIteration

    def __getitem__(self, idx: int) -> Any:
        if idx >= len(self.data):
            raise IndexError
        return self.data[idx]

    def __abs__(self) -> 'Vector':
        return Vector(data=[abs(item) for item in self.data],
                      is_permissive=self.is_permissive)

    def __add__(self, other: 'Vector') -> 'Vector':
        if not isinstance(other, Vector):
            return NotImplemented

        result = Vector(is_permissive=self.is_permissive)
        result.data = [x + y for x, y in
                       vector_pairs(self, other, self.is_permissive)]
        return result

    def __sub__(self, other: 'Vector') -> 'Vector':
        if not isinstance(other, Vector):
            return NotImplemented

        result = Vector(is_permissive=self.is_permissive)
        result.data = [x - y for x, y in
                       vector_pairs(self, other, self.is_permissive)]
        return result

    def __mul__(self, other: Any) -> 'Vector':
        if not isinstance(other, int) and \
                not isinstance(other, float) and \
                not isinstance(other, Vector):
            return NotImplemented

        result = Vector(is_permissive=self.is_permissive)

        if isinstance(other, Vector):
            result.data = [x * y for x, y in
                           vector_pairs(self, other, self.is_permissive)]
        else:
            result.data = [other * item for item in self.data]

        return result

    def __pow__(self, other: int) -> 'Vector':
        if not isinstance(other, int):
            return NotImplemented

        result = Vector(data=self.data, is_permissive=self.is_permissive)
        for _ in range(other - 1):
            result = result * result
        return result


class Coordinate(JsonSerializable, Vector):
    def __init__(self, latitude: float, longitude: float):
        JsonSerializable.__init__(self)
        Vector.__init__(self, data=[latitude, longitude])

        self.latitude = latitude
        self.longitude = longitude

    def __eq__(self, other: 'Coordinate') -> bool:
        if not isinstance(other, Coordinate):
            return NotImplemented
        return self.latitude == other.latitude and self.longitude == other.longitude

    def __ne__(self, other: 'Coordinate') -> bool:
        return not self.__eq__(other)

    def __abs__(self) -> 'Coordinate':
        vector = Vector.__abs__(self)
        return Coordinate(vector.data[0], vector.data[1])

    def __add__(self, other: 'Coordinate') -> 'Coordinate':
        vector = Vector.__add__(self, other)
        return Coordinate(vector.data[0], vector.data[1])

    def __sub__(self, other: 'Coordinate') -> 'Coordinate':
        vector = Vector.__sub__(self, other)
        return Coordinate(vector.data[0], vector.data[1])

    def __mul__(self, other: Any) -> 'Coordinate':
        vector = Vector.__mul__(self, other)
        return Coordinate(vector.data[0], vector.data[1])

    def __pow__(self, other: int) -> 'Coordinate':
        vector = Vector.__pow__(self, other)
        return Coordinate(vector.data[0], vector.data[1])

    def __repr__(self) -> str:
        return f'Coordinate(latitude={self.latitude}, longitude={self.longitude})'

    def distance(self, other: 'Coordinate') -> float:
        R = 6373.0

        lat1 = radians(self.latitude)
        lon1 = radians(self.longitude)
        lat2 = radians(other.latitude)
        lon2 = radians(other.longitude)

        dlon = lon2 - lon1
        dlat = lat2 - lat1

        a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
        c = 2 * atan2(sqrt(a), sqrt(1 - a))

        return R * c

    def heading(self, other: 'Coordinate') -> float:
        lat1 = radians(self.latitude)
        lon1 = radians(self.longitude)
        lat2 = radians(other.latitude)
        lon2 = radians(other.longitude)

        y = sin(lon2 - lon1) * cos(lat2)
        x = cos(lat1) * sin(lat2) - sin(lat1) * cos(lat2) * cos(lon2 - lon1)

        initial_bearing = degrees(atan2(y, x))
        compass_bearing = (initial_bearing + 360) % 360

        return compass_bearing

    def create_at(self, distance: float, heading: float):
        R = 6373.0

        lat1 = radians(self.latitude)
        lon1 = radians(self.longitude)
        distance /= R
        heading = radians(heading)

        lat2 = asin(sin(lat1) * cos(distance) +
                    cos(lat1) * sin(distance) * cos(heading))
        lon2 = lon1 + atan2(sin(heading) * sin(distance) * cos(lat1),
                            cos(distance) - sin(lat1) * sin(lat2))
        lon2 = (lon2 + 3 * pi) % (2 * pi) - pi

        return Coordinate(degrees(lat2), degrees(lon2))

    def to_json(self):
        return {
            'mc_model': self.mc_model,
            'latitude': self.latitude,
            'longitude': self.longitude
        }

    @staticmethod
    def from_json(obj: dict) -> 'Coordinate':
        lat = obj['latitude']
        lon = obj['longitude']

        return Coordinate(lat, lon)


class Point(JsonSerializable, Vector):
    def __init__(self, id_: str, position: Coordinate):
        JsonSerializable.__init__(self)
        Vector.__init__(self, data=[position.latitude, position.longitude])

        self.id_ = id_
        self.timestamp = datetime.utcnow()
        self.position = position
        self.heading = 0

    def __eq__(self, other: 'Point') -> bool:
        if not isinstance(other, Point):
            return NotImplemented
        return self.position == other.position and self.heading == other.heading

    def __ne__(self, other: 'Point') -> bool:
        return not self.__eq__(other)

    def __abs__(self) -> 'Point':
        vector = Vector.__abs__(self)
        coordinate = Coordinate(vector.data[0], vector.data[1])
        return Point(id_=None, position=coordinate)

    def __add__(self, other: 'Point') -> 'Point':
        vector = Vector.__add__(self, other)
        coordinate = Coordinate(vector.data[0], vector.data[1])
        return Point(id_=None, position=coordinate)

    def __sub__(self, other: 'Point') -> 'Point':
        vector = Vector.__sub__(self, other)
        coordinate = Coordinate(vector.data[0], vector.data[1])
        return Point(id_=None, position=coordinate)

    def __mul__(self, other: Any) -> 'Point':
        vector = Vector.__mul__(self, other)
        coordinate = Coordinate(vector.data[0], vector.data[1])
        return Point(id_=None, position=coordinate)

    def __pow__(self, other: int) -> 'Point':
        vector = Vector.__pow__(self, other)
        coordinate = Coordinate(vector.data[0], vector.data[1])
        return Point(id_=None, position=coordinate)

    def __repr__(self) -> str:
        return f'Point(position={self.position}, heading={self.heading})'

    def to_json(self):
        return {
            'mc_model': self.mc_model,
            'id': self.id_,
            'position': self.position.to_json(),
            'heading': self.heading
        }

    @staticmethod
    def from_json(obj: dict) -> 'Point':
        id_ = obj['id']
        heading = obj['heading']
        position = obj['position']
        position = Coordinate.from_json(position) if isinstance(
            position, dict) else position

        point = Point(id_, position)
        point.heading = heading

        return point


class Path(JsonSerializable):
    def __init__(self):
        super().__init__()

        self.id_ = None
        self.points = []
        self.iterator = 0

    def add_point(self, point: Point):
        if self.id_ is None:
            self.id_ = point.id_
        if self.id_ == point.id_:
            heading = 0

            if self.points:
                last_point = self.points[-1]
                heading = last_point.position.heading(point.position)
                last_point.heading = heading

            if heading is not None:
                point.heading = heading

            self.points.append(point)

    def length(self) -> float:
        return sum([self.points[i].position.distance(self.points[i + 1].position) for i in range(len(self.points) - 1)])

    def __iter__(self):
        self.iterator = 0
        return self

    def __next__(self):
        if self.iterator < len(self.points):
            point = self.points[self.iterator]
            self.iterator = self.iterator + 1
            return point
        else:
            raise StopIteration

    def __eq__(self, other: 'Path') -> bool:
        if not isinstance(other, Path):
            return NotImplemented
        return self.id_ == other.id_ and \
            len(self.points) == len(other.points) and \
            all(p == op for p, op in zip(self.points, other.points))

    def __ne__(self, other: 'Path') -> bool:
        return not self.__eq__(other)

    def __repr__(self) -> str:
        return f'Path(points=[{", ".join(repr(point) for point in self.points)}])'

    def to_json(self):
        return {
            'mc_model': self.mc_model,
            'id': self.id_,
            'points': [point.to_json() for point in self.points]
        }

    @staticmethod
    def from_json(obj: dict) -> 'Path':
        id_ = obj['id']
        points = [Point.from_json(json_) if isinstance(
            json_, dict) else json_ for json_ in obj['points']]

        path = Path()
        path.id_ = id_
        path.points = points

        return path


class Egress(Path):
    def __init__(self):
        super().__init__()

    def __eq__(self, other: 'Egress') -> bool:
        if not isinstance(other, Egress):
            return NotImplemented
        return super().__eq__(other)

    def __ne__(self, other: 'Egress') -> bool:
        return not self.__eq__(other)

    def __repr__(self) -> str:
        return f'Egress(points=[{", ".join(repr(point) for point in self.points)}])'

    @staticmethod
    def from_json(obj: dict) -> 'Egress':
        id_ = obj['id']
        points = [Point.from_json(json_) if isinstance(
            json_, dict) else json_ for json_ in obj['points']]

        egress = Egress()
        egress.id_ = id_
        egress.points = points

        return egress

    @staticmethod
    def from_path(path: 'Path') -> 'Egress':
        egress = Egress()
        egress.id_ = path.id_
        egress.points = path.points
        return egress


class Ingress(Path):
    def __init__(self):
        super().__init__()
        self.egresses = []

    def add_egress(self, egress: Egress):
        self.egresses.append(egress)

    def __eq__(self, other: 'Ingress') -> bool:
        if not isinstance(other, Path):
            return NotImplemented
        return super().__eq__(other) and \
            len(self.egresses) == len(other.egresses) and \
            all(e == oe for e, oe in zip(self.egresses, other.egresses))

    def __ne__(self, other: 'Ingress') -> bool:
        return not self.__eq__(other)

    def __repr__(self) -> str:
        return f'Ingress(points=[{", ".join(repr(point) for point in self.points)}], ' \
            + f'egresses=[{", ".join(repr(egress) for egress in self.egresses)}])'

    def to_json(self) -> str:
        return {
            'mc_model': self.mc_model,
            'id': self.id_,
            'points': [point.to_json() for point in self.points],
            'egresses': [egress.to_json() for egress in self.egresses]
        }

    @staticmethod
    def from_json(obj: dict) -> 'Ingress':
        id_ = obj['id']
        points = [Point.from_json(json_) if isinstance(
            json_, dict) else json_ for json_ in obj['points']]
        egresses = [Egress.from_json(json_) if isinstance(
            json_, dict) else json_ for json_ in obj['egresses']]

        ingress = Ingress()
        ingress.id_ = id_
        ingress.points = points
        ingress.egresses = egresses

        return ingress

    @staticmethod
    def from_path(path: 'Path') -> 'Ingress':
        ingress = Ingress()
        ingress.id_ = path.id_
        ingress.points = path.points
        return ingress


class Map(JsonSerializable):
    def __init__(self, ref_point: Coordinate, ingresses: List[Ingress]):
        super().__init__()

        self.ref_point = ref_point
        self.ingresses = ingresses

    def to_map_message(self):
        pass

    def __eq__(self, other: 'Map') -> bool:
        if not isinstance(other, Map):
            return NotImplemented
        return self.ref_point == other.ref_point and \
            len(self.ingresses) == len(other.ingresses) and \
            all(i == oi for i, oi in zip(self.ingresses, other.ingresses))

    def __ne__(self, other: 'Map') -> bool:
        return not self.__eq__(other)

    def __repr__(self):
        return f'Map(ref_point={self.ref_point}, ingresses=[{", ".join(repr(ingress) for ingress in self.ingresses)}])'

    def to_json(self):
        return {
            'mc_model': self.mc_model,
            'ref_point': self.ref_point.to_json(),
            'ingresses': [ingress.to_json() for ingress in self.ingresses]
        }

    @staticmethod
    def from_json(obj: dict) -> 'Map':
        ref_point = obj['ref_point']
        ref_point = Coordinate.from_json(ref_point) if isinstance(
            ref_point, dict) else ref_point
        ingresses = [Ingress.from_json(json_) if isinstance(
            json_, dict) else json_ for json_ in obj['ingresses']]

        return Map(ref_point, ingresses)


class ModelJSONEncoder(json.JSONEncoder):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def default(self, obj):
        if isinstance(obj, (Coordinate,
                            Egress,
                            Ingress,
                            Map,
                            Path,
                            Point)):
            return obj.to_json()
        return super().default(obj)


class ModelJSONDecoder(json.JSONDecoder):
    def __init__(self):
        super().__init__(object_hook=self.object_hook)

    def object_hook(self, obj):
        if 'mc_model' in obj:
            class_ = obj['mc_model']

            if class_ == 'Coordinate':
                return Coordinate.from_json(obj)
            elif class_ == 'Egress':
                return Egress.from_json(obj)
            elif class_ == 'Ingress':
                return Ingress.from_json(obj)
            elif class_ == 'Map':
                return Map.from_json(obj)
            elif class_ == 'Path':
                return Path.from_json(obj)
            elif class_ == 'Point':
                return Point.from_json(obj)

        return obj
