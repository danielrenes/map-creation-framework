#!/usr/bin/env python

# pylint: disable=C0103

import time

from map_creator.model import Coordinate, Egress, Ingress, Point, Map
from map_creator.wrapper import WrappedMap
from map_creator.server import DebugHTTPServer

server_1 = DebugHTTPServer(port=31289)
server_2 = DebugHTTPServer(port=31290)

range_1 = 1.0
ref_point_1 = Coordinate(47.47687, 19.05075)
egress_1_1_1 = Egress()
egress_1_1_1.add_point(Point(11, Coordinate(47.47690, 19.05068)))
egress_1_1_1.add_point(Point(11, Coordinate(47.47707, 19.05012)))
egress_1_1_2 = Egress()
egress_1_1_2.add_point(Point(12, Coordinate(47.47672, 19.05072)))
egress_1_1_2.add_point(Point(12, Coordinate(47.47644, 19.05064)))
ingress_1_1 = Ingress()
ingress_1_1.add_point(Point(1, Coordinate(47.47665, 19.05156)))
ingress_1_1.add_point(Point(1, Coordinate(47.47685, 19.05086)))
ingress_1_1.add_egress(egress_1_1_1)
ingress_1_1.add_egress(egress_1_1_2)
egress_1_2_1 = Egress()
egress_1_2_1.add_point(Point(21, Coordinate(47.47690, 19.05068)))
egress_1_2_1.add_point(Point(21, Coordinate(47.47705, 19.05018)))
ingress_1_2 = Ingress()
ingress_1_2.add_point(Point(2, Coordinate(47.47742, 19.05093)))
ingress_1_2.add_point(Point(2, Coordinate(47.47694, 19.05077)))
ingress_1_2.add_egress(egress_1_2_1)
ingresses_1 = [ingress_1_1, ingress_1_2]
map_1 = Map(ref_point_1, ingresses_1)
wrapped_map_1 = WrappedMap(map_1)

server_1._rsu_info = {
    'ref_point': {
        'latitude': ref_point_1.latitude,
        'longitude': ref_point_1.longitude
    },
    'range': range_1
}

server_1._latest_map = wrapped_map_1.to_json()


range_2 = 1.0
ref_point_2 = Coordinate(47.47735, 19.05358)
egress_2_1_1 = Egress()
egress_2_1_1.add_point(Point(31, Coordinate(47.47736, 19.05372)))
egress_2_1_1.add_point(Point(31, Coordinate(47.47740, 19.05430)))
ingress_2_1 = Ingress()
ingress_2_1.add_point(Point(3, Coordinate(47.47748, 19.05298)))
ingress_2_1.add_point(Point(3, Coordinate(47.47738, 19.05346)))
ingress_2_1.add_egress(egress_2_1_1)
egress_2_2_1 = Egress()
egress_2_2_1.add_point(Point(41, Coordinate(47.47745, 19.05359)))
egress_2_2_1.add_point(Point(41, Coordinate(47.47779, 19.05362)))
ingress_2_2 = Ingress()
ingress_2_2.add_point(Point(4, Coordinate(47.47702, 19.05349)))
ingress_2_2.add_point(Point(4, Coordinate(47.47731, 19.05355)))
ingress_2_2.add_egress(egress_2_2_1)
ingresses_2 = [ingress_2_1, ingress_2_2]
map_2 = Map(ref_point_2, ingresses_2)
wrapped_map_2 = WrappedMap(map_2)

server_2._rsu_info = {
    'ref_point': {
        'latitude': ref_point_2.latitude,
        'longitude': ref_point_2.longitude
    },
    'range': range_2
}

server_2._latest_map = wrapped_map_2.to_json()

server_1.start()
server_2.start()

try:
    while True:
        time.sleep(0.1)
except KeyboardInterrupt:
    server_1.stop()
    server_2.stop()
