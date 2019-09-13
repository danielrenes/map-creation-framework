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


def find_key_points(path: 'Path') -> 'Path':
    '''Find the key points on the path and return a new path
    created from those key points.

    Args:
        path (Path): the path

    Returns:
        Path: the path from the key points of the input path
    '''

    if len(path.points) <= 2:
        return path

    max_diff_heading = 4

    out_path = Path()
    out_path.add_point(path.points[0])

    for i in range(1, len(path.points) - 1):
        curr_point = path.points[i - 1]
        next_point = path.points[i]

        if abs(next_point.heading - curr_point.heading) > max_diff_heading:
            out_path.add_point(next_point)

    out_path.add_point(path.points[-1])

    return out_path


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


def condense(path: 'Path', number_of_points: int = 50) -> 'Path':
    if len(path.points) < 2 or len(path.points) >= number_of_points:
        return path

    distances = [path.points[i].position.distance(path.points[i + 1].position)
                 for i in range(len(path.points) - 1)]

    length = sum(distances)

    if length == 0:
        return path

    number_of_points = number_of_points - len(path.points)
    number_of_points_per_segment = [distance / length * number_of_points
                                    for distance in distances]

    floating_parts = [n for n in number_of_points_per_segment]
    number_of_points_per_segment = [int(n) for n in
                                    number_of_points_per_segment]
    floating_parts = [f - n for f, n in
                      zip(floating_parts, number_of_points_per_segment)]

    while sum(number_of_points_per_segment) < number_of_points:
        index = floating_parts.index(max(floating_parts))
        number_of_points_per_segment[index] = number_of_points_per_segment[index] + 1

    out_path = Path()

    for i, n_points in enumerate(number_of_points_per_segment):
        if n_points == 0:
            continue

        last_point = path.points[i]
        step = distances[i] / n_points
        heading = last_point.heading

        out_path.add_point(last_point)

        for _ in range(n_points):
            new_point = Point(
                path.id_, last_point.position.create_at(step, heading))
            out_path.add_point(new_point)
            last_point = new_point

    out_path.add_point(path.points[-1])

    return out_path

# def adjust(path_1: 'Path', path_2: 'Path') -> Tuple['Path', 'Path']:
#     closest_points = None
#     min_distance = 100000

#     for point_1 in path_1.points:
#         closest_point_2 = closest_point(point_1, path_2.points)
#         distance = point_1.position.distance(closest_point_2.position)

#         if distance < min_distance:
#             closest_points = (point_1, closest_point_2)
#             min_distance = distance

#     if not closest_points:
#         return (path_1, path_2)

#     index_1 = path_1.points.index(closest_points[0])
#     index_2 = path_2.points.index(closest_points[1])

#     points_1, points_2 = [], []

#     curr_point_1, curr_point_2 = closest_points
#     i, j = index_1 - 1, index_2 - 1

#     if i >= 0 and j >= 0:
#         previous_point_1, previous_point_2 = path_1.points[i], path_2.points[j]

#     while i >= 0 and j >= 0:
#         distance_1 = curr_point_1.position.distance(previous_point_1.position)
#         distance_2 = curr_point_2.position.distance(previous_point_2.position)

#         if (distance_1 > distance_2):
#             heading = curr_point_1.position.heading(previous_point_1.position)
#             new_point = Point(path_1.id_, curr_point_1.position.create_at(distance_2, heading))
#             points_1.append(new_point)
#             points_2.append(previous_point_2)

#             curr_point_1 = new_point
#             i = i - 1
#             if i >= 0:
#                 previous_point_1 = path_1.points[i]

#             j = j - 1
#             if j >= 0:
#                 curr_point_2 = path_2.points[j]

#             j = j - 1
#             if j >= 0:
#                 previous_point_2 = path_2.points[j]
#         else:
#             i = i - 1
#             heading = curr_point_2.position.heading(previous_point_2.position)
#             new_point = Point(path_2.id_, curr_point_2.position.create_at(distance_1, heading))
#             points_2.append(new_point)
#             previous_point_2 = new_point

#             points_1.append(previous_point_1)
#             if i >= 0:
#                 previous_point_1 = path_1.points[i]

#     points_1, points_2 = list(reversed(points_1)), list(reversed(points_2))

#     points_1.append(closest_points[0])
#     points_2.append(closest_points[1])

#     index_1 = path_1.points.index(closest_points[0])
#     index_2 = path_2.points.index(closest_points[1])

#     curr_point_1, curr_point_2 = closest_points
#     i, j = index_1 + 1, index_2 + 1

#     if i < len(path_1.points) and j < len(path_2.points):
#         next_point_1, next_point_2 = path_1.points[i], path_2.points[j]

#     while i < len(path_1.points) and j < len(path_2.points):
#         distance_1 = curr_point_1.position.distance(next_point_1.position)
#         distance_2 = curr_point_2.position.distance(next_point_2.position)

#         if (distance_1 > distance_2):
#             j = j + 1
#             heading = curr_point_1.position.heading(next_point_1.position)
#             new_point = Point(path_1.id_, curr_point_1.position.create_at(distance_2, heading))
#             points_1.append(new_point)
#             next_point_1 = new_point

#             points_2.append(next_point_2)
#             if j < len(path_2.points):
#                 next_point_2 = path_2.points[j]
#         else:
#             i = i + 1
#             heading = curr_point_2.position.heading(next_point_2.position)
#             new_point = Point(path_2.id_, curr_point_2.position.create_at(distance_1, heading))
#             points_2.append(new_point)
#             next_point_2 = new_point

#             points_1.append(next_point_1)
#             if i < len(path_1.points):
#                 next_point_1 = path_1.points[i]

#     out_path_1, out_path_2 = Path(), Path()

#     for point in points_1:
#         out_path_1.add_point(point)

#     for point in points_2:
#         out_path_2.add_point(point)

#     return (out_path_1, out_path_2)
