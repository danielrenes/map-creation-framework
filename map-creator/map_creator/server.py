import json
import logging
from http.server import HTTPServer, BaseHTTPRequestHandler
import time
import threading

LOGGER = logging.getLogger(__name__)


class DebugHTTPServer(HTTPServer):
    class HTTPRequestHandler(BaseHTTPRequestHandler):
        RESPONSE = {
            '/': 'rsu_info',
            '/map': 'latest_map',
            '/ping': None
        }

        def _make_json_response(self, obj):
            if obj:
                return json.dumps(obj)
            return json.dumps({})

        def _set_headers(self):
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()

        def do_GET(self):
            if self.path in self.RESPONSE:
                attr = self.RESPONSE[self.path]
                obj = None

                if attr is not None and hasattr(self.server, attr):
                    obj = getattr(self.server, attr)

                response = self._make_json_response(obj)

                self._set_headers()
                self.wfile.write(response.encode())

    def __init__(self, host='localhost', port: int = 31289):
        server_address = (host, port)
        handler = DebugHTTPServer.HTTPRequestHandler

        super().__init__(server_address, handler)
        self.socket.setblocking(0)

        self._rsu_info = None
        self._latest_map = None

        self._thread = threading.Thread(target=self.serve_forever)
        self._thread.daemon = True
        self._terminate = threading.Event()

        LOGGER.info(f'Initialized debug server on {host}:{port}')

    @property
    def rsu_info(self):
        return self._rsu_info

    @rsu_info.setter
    def rsu_info(self, val):
        self._rsu_info = val

    @property
    def latest_map(self):
        return self._latest_map

    @latest_map.setter
    def latest_map(self, val):
        self._latest_map = val

    def start(self):
        self._thread.start()
        LOGGER.info('Started debug server')

    def stop(self):
        self._terminate.set()
        self._thread.join()
        LOGGER.info('Stopped debug server')

    def serve_forever(self):
        while not self._terminate.is_set():
            self.handle_request()
            time.sleep(0.1)
