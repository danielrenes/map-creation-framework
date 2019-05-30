from .model import Coordinate, Egress, Ingress, JsonSerializable, Map, Path, Point


class Wrapper(JsonSerializable):
    def __init__(self, obj: object):
        if not issubclass(obj.__class__, JsonSerializable):
            raise TypeError('Wrapped object must be JsonSerializable')

        super().__init__()

        self.obj = obj

    def __eq__(self, other) -> bool:
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.obj == other.obj

    def __ne__(self, other) -> bool:
        return not self.__eq__(other)

    def to_json(self):
        dict_ = self.obj.to_json()
        dict_.pop('mc_model')
        return dict_

    @staticmethod
    def from_json(obj):
        if not 'mc_model' in obj:
            raise AttributeError('Dict must contain mc_model')

        mc_model = obj['mc_model']
        wrapped_class = None
        wrapper_class = None

        if mc_model == 'Coordinate':
            wrapped_class = Coordinate
            wrapper_class = WrappedCoordinate
        elif mc_model == 'Egress':
            wrapped_class = Egress
            wrapper_class = WrappedEgress
        elif mc_model == 'Ingress':
            wrapped_class = Ingress
            wrapper_class = WrappedIngress
        elif mc_model == 'Map':
            wrapped_class = Map
            wrapper_class = WrappedMap
        elif mc_model == 'Path':
            wrapped_class = Path
            wrapper_class = WrappedPath
        elif mc_model == 'Point':
            wrapped_class = Point
            wrapper_class = WrappedPoint
        else:
            raise TypeError(f'Wrapper not implemented for {mc_model}')

        wrapped_object = wrapped_class.from_json(obj)

        return wrapper_class(wrapped_object)


class WrappedCoordinate(Wrapper):
    def __init__(self, coordinate: 'Coordinate'):
        super().__init__(coordinate)

    def to_json(self):
        return super().to_json()


class WrappedPoint(Wrapper):
    def __init__(self, point: 'Point'):
        super().__init__(point)

    def to_json(self):
        dict_ = super().to_json()

        wrapped_coordinate = WrappedCoordinate.from_json(dict_['position'])

        dict_ = wrapped_coordinate.to_json()

        return dict_


class WrappedPath(Wrapper):
    def __init__(self, path: 'Path'):
        super().__init__(path)

    def to_json(self):
        dict_ = super().to_json()

        wrapped_points = [WrappedPoint.from_json(
            point) for point in dict_['points']]

        dict_ = [wrapped_point.to_json()
                 for wrapped_point in wrapped_points]

        return dict_


class WrappedEgress(WrappedPath):
    def __init__(self, egress: Egress):
        super().__init__(egress)


class WrappedIngress(Wrapper):
    def __init__(self, ingress: Ingress):
        super().__init__(ingress)

    def to_json(self):
        dict_ = super().to_json()

        dict_.pop('id')

        wrapped_points = [WrappedPoint.from_json(
            point) for point in dict_['points']]

        dict_['points'] = [wrapped_point.to_json()
                           for wrapped_point in wrapped_points]

        wrapped_egresses = [WrappedEgress.from_json(
            egress) for egress in dict_['egresses']]

        dict_['egresses'] = [wrapped_egress.to_json()
                             for wrapped_egress in wrapped_egresses]

        return dict_


class WrappedMap(Wrapper):
    def __init__(self, map_data: Map):
        super().__init__(map_data)

    def to_json(self):
        dict_ = super().to_json()

        wrapped_coordinate = WrappedCoordinate.from_json(dict_['ref_point'])

        wrapped_ingresses = [WrappedIngress.from_json(
            ingress) for ingress in dict_['ingresses']]

        dict_['ref_point'] = wrapped_coordinate.to_json()
        dict_['ingresses'] = [wrapped_ingress.to_json()
                              for wrapped_ingress in wrapped_ingresses]

        return dict_
