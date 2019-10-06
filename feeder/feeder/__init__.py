from enum import Enum


class Closable:
    def close(self):
        raise NotImplementedError


class Runner(Closable):
    def __init__(self):
        self.delay = 1

    def run(self) -> bool:
        raise NotImplementedError


class Mode(Enum):
    FEED = 'feed'
    GENERATE = 'generate'

    def __str__(self):
        return self.value
