import json
import time

from feeder.factory import Factory


config_path = './config.json'


def read_config(path: str) -> dict:
    with open(path, 'r') as f:
        return json.loads(f.read())


config = read_config(config_path)

queue, runner = Factory.create(config)

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
