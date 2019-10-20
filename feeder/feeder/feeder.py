from . import Runner


class Feeder(Runner):
    def __init__(self, reader: 'Reader', queue: 'Queue'):
        super().__init__()

        self.reader = reader
        self.queue = queue

    def feed(self) -> bool:
        objs = self.reader.get_next()

        if not objs:
            return False

        for obj in objs:
            self.queue.put(obj.encode())

        return True

    def run(self) -> bool:
        return self.feed()

    def close(self):
        self.reader.close()
