import json
import sys
import time

from feeder.factory import Factory


config_path = './config.json'


def read_config(path: str) -> dict:
    if sys.stdin.isatty():
        with open(path, 'r') as f:
            return json.loads(f.read())
    else:
        return json.loads(''.join(sys.stdin.readlines()))


config = read_config(config_path)

queue, runner = Factory.create(config)

if queue:
    queue.open()

try:
    while runner.run():
        if runner.delay > 0:
            time.sleep(runner.delay)
except KeyboardInterrupt:
    pass
finally:
    if queue:
        queue.close()
    runner.close()
