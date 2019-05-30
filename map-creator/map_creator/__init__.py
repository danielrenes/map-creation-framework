import logging

# logging level will be configurable

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s %(funcName)-12s %(lineno)-4d %(levelname)-8s %(message)s'
)