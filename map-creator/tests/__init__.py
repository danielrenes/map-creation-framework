import logging
from unittest import TestCase

class NoLoggingTestCase(TestCase):
    def setUp(self):
        logging.disable(logging.CRITICAL)

    def tearDown(self):
        logging.disable(logging.NOTSET)