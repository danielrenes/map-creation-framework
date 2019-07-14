import argparse
import time

from feeder import Mode
from feeder.factory import Factory


parser = argparse.ArgumentParser()
parser.add_argument('mode', type=Mode, choices=list(Mode))

args = parser.parse_args()

# config = {
#     'source': 'csv',
#     'mapping': {
#         'identifier': 'id',
#         'latitude': 'latitude',
#         'longitude': 'longitude'
#     },
#     'filepath': '/home/rd/Documents/Diplomamunka/0_FINAL/go_track_trackpoints.csv'
# }

config = {
    'source': 'sumo',
    'mapping': {
        'identifier': 'id',
        'latitude': 'latitude',
        'longitude': 'longitude'
    },
    'sumocfg_path': '/home/rd/Documents/Diplomamunka/0_FINAL/map-creation-framework/simulations/1/map.sumocfg'
}

queue, runner = Factory.create(args.mode, config)

if queue:
    queue.open()

try:
    while runner.run():
        time.sleep(1)
except KeyboardInterrupt:
    pass
finally:
    if queue:
        queue.close()
    runner.close()
