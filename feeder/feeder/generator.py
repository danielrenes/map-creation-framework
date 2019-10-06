import os

from . import Runner


class Generator(Runner):
    def __init__(self, reader: 'Reader', out_file: str):
        self.reader = reader
        self.out_file = out_file
        self.delay = 0

        if os.path.exists(self.out_file):
            os.remove(self.out_file)

    def generate(self) -> bool:
        with open(self.out_file, 'a') as f:
            if self.reader.is_finished:
                return False

            objs = self.reader.get_next()

            if objs:
                for obj in objs:
                    f.write(f'{obj.encode()}\n')

            return True

    def run(self) -> bool:
        return self.generate()

    def close(self):
        self.reader.close()
