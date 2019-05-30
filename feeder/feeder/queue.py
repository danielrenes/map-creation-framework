import json
import time
import threading
import socket


def non_blocking_lock(lock):
    def outer(function):
        def inner(*args, **kwargs):
            l = getattr(args[0], lock)
            if l.acquire(False):
                try:
                    return function(*args, **kwargs)
                finally:
                    l.release()
        return inner
    return outer


class Queue:
    def __init__(self, host: str = 'localhost', port: int = 51836, max_size: int = 50):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.setblocking(0)
        self.sock.bind((host, port))
        self.max_data_size = 1024
        self.max_transmit_count = 10
        self.queue = []
        self.max_queue_size = max_size
        self.connections = []

        self.queue_lock = threading.Lock()
        self.connections_lock = threading.Lock()
        self.stop_event = threading.Event()
        self.server_thread = threading.Thread(target=self.run_server_thread)
        self.server_thread.daemon = True

    @non_blocking_lock('queue_lock')
    def put(self, obj: object):
        while len(self.queue) >= self.max_queue_size:
            self.queue.pop(0)
        self.queue.append(obj)

    def open(self):
        self.server_thread.start()

    def close(self):
        self.stop_event.set()
        self.server_thread.join()
        self.sock.close()

    @non_blocking_lock('connections_lock')
    def add_connection(self, addr):
        print('New connection:', addr)
        self.connections.append(addr)

    @non_blocking_lock('connections_lock')
    def remove_connection(self, addr):
        if addr in self.connections:
            print('Disconnected:', addr)
            self.connections.remove(addr)

    @non_blocking_lock('queue_lock')
    @non_blocking_lock('connections_lock')
    def send_data(self):
        data = []
        index = 0
        queue_size = len(self.queue)
        while index < queue_size:
            item = self.queue[index]
            if len(data) < self.max_transmit_count:
                data.append(item)
            if len(data) == self.max_transmit_count or index == (queue_size - 1):
                for connection in self.connections:
                    json_str = json.dumps(data)
                    self.sock.sendto(json_str.encode(), connection)
                data.clear()
            index += 1
        print('Sent data to', self.connections)
        self.queue.clear()

    def run_server_thread(self):
        while not self.stop_event.is_set():
            data, addr = None, None

            try:
                data, addr = self.sock.recvfrom(self.max_data_size)
            except BlockingIOError:
                pass

            if data and addr:
                print(f'Received from {addr}: {data}')
                if data == b'connect':
                    self.add_connection(addr)
                elif data == b'disconnect':
                    self.remove_connection(addr)

            try:
                self.send_data()
            except BlockingIOError:
                pass

            time.sleep(0.1)
