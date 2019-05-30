from typing import List, Tuple

from .model import Coordinate, Egress, Ingress, Path, Point


def closest_point(target: 'Point', points: List['Point']):
    '''Find the point in the input points that is closest to the target

    Args:
        target (Point): the target point
        points (List[Point]): the input points

    Returns:
        Point: the point that is closest to the target
    '''

    closest = None
    min_distance = None

    for point in points:
        distance = target.position.distance(point.position)
        if min_distance is None or distance < min_distance:
            min_distance = distance
            closest = point

    return closest


def split_path(splitter: 'Point', path: 'Path') -> Tuple['Ingress', 'Egress']:
    '''Split the input path into an ingress and an egress part at the closest point to the given splitter.
    Add the egress to the egresses list of the ingress.

    Args:
        splitter (Point): the split point
        path (Path): the path

    Returns:
        (Ingress, Egress): the ingress and egress part of the path
    '''

    ingress = Ingress()
    egress = Egress()
    reached_split = False

    split_point = closest_point(splitter, path.points)

    for point in path.points:
        if reached_split:
            egress.add_point(point)
        else:
            ingress.add_point(point)

        if not reached_split and point == split_point:
            reached_split = True

    return (ingress, egress)


def interpolate(path: 'Path', num_of_points: int) -> 'Path':
    '''Interpolate the input path to contain num_of_points points at even distances.
    Keeps the first and last points of the path.

    Args:
        path (Path): the input path

    Returns:
        Path: the interpolated path
    '''

    if len(path.points) < 2:
        return path

    curr_point = path.points[0]

    interpolated = Path()
    interpolated.add_point(path.points[0])

    distance = path.length() / num_of_points
    index = 1
    next_point = path.points[index]

    while index < len(path.points) - 1 or len(interpolated.points) < num_of_points - 1:
        if curr_point.position.distance(next_point.position) < distance:
            index += 1
            next_point = path.points[index]
        else:
            heading = curr_point.position.heading(next_point.position)
            new_coordinate = curr_point.position.create_at(
                distance, heading)
            new_point = Point(path.id_, new_coordinate)
            interpolated.add_point(new_point)
            curr_point = new_point

    interpolated.add_point(path.points[-1])

    return interpolated


def combine_paths(paths: List['Path']) -> 'Path':
    if len(paths) == 1:
        return paths[0]

    combined = Path()
    id_ = None

    min_lat, min_lon, max_lat, max_lon, resolution = 1000, 1000, 0, 0, 0

    for path in paths:
        if not id_:
            id_ = path.id_

        if len(path.points) > resolution:
            resolution = len(path.points)

        for point in path.points:
            if point.position.latitude < min_lat:
                min_lat = point.position.latitude
            if point.position.longitude < min_lon:
                min_lon = point.position.longitude
            if point.position.latitude > max_lat:
                max_lat = point.position.latitude
            if point.position.longitude > max_lon:
                max_lon = point.position.longitude

    resolution = resolution * 2
    min_lat = int(min_lat * 1e6)
    min_lon = int(min_lon * 1e6)
    max_lat = int(max_lat * 1e6)
    max_lon = int(max_lon * 1e6)

    step_lat = max(1, int((max_lat - min_lat) / resolution))
    step_lon = max(1, int((max_lon - min_lon) / resolution))

    for lat, lon in zip(range(min_lat, max_lat, step_lat), range(min_lon, max_lon, step_lon)):
        target = Point(None, Coordinate(lat / 1e6, lon / 1e6))
        closest_points = [closest_point(target, path.points)
                          for path in paths]
        avg_lat = sum(
            point.position.latitude for point in closest_points) / len(closest_points)
        avg_lon = sum(
            point.position.longitude for point in closest_points) / len(closest_points)
        point = Point(id_, Coordinate(avg_lat, avg_lon))

        if not combined.points or point.position != combined.points[-1].position:
            combined.add_point(point)

    return combined
