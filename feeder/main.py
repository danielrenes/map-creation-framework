import time

from feeder.factory import Factory

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
    'sumocfg_path': '/home/rd/Documents/Diplomamunka/0_FINAL/simulations/1/map.sumocfg'
}

queue, feeder = Factory.create(config)

queue.open()

try:
    while feeder.feed():
        time.sleep(1)
except KeyboardInterrupt:
    pass
finally:
    queue.close()
    feeder.close()