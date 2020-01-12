#!/usr/bin/env python3

SYSLOG_LISTEN_HOST = "0.0.0.0"
SYSLOG_LISTEN_PORT = 514

DUMP_LISTEN_HOST = "0.0.0.0"
DUMP_LISTEN_PORT = 8098

MAX_LOGS = 10000

import socketserver
import threading
import time

lock = threading.Lock()
logs = []

class SyslogHandler(socketserver.BaseRequestHandler):
    def handle(self):
        global logs
        client = str(self.client_address)
        msg = str(self.request[0].strip())
        logs.append(f'{client}: {msg}')
        with lock:
            logs = logs[-MAX_LOGS:]

class DumpHandler(socketserver.StreamRequestHandler):
    def handle(self):
        self.wfile.write('logs\n'.encode('utf8'))
        with lock:
            for l in logs:
                self.wfile.write((l + '\n').encode('utf8'))

if __name__ == "__main__":
    syslog_server = socketserver.UDPServer((SYSLOG_LISTEN_HOST, SYSLOG_LISTEN_PORT), SyslogHandler)
    dump_server = socketserver.TCPServer((DUMP_LISTEN_HOST, DUMP_LISTEN_PORT), DumpHandler)
    dump_server.allow_reuse_address = True

    threads = []
    for server in (syslog_server, dump_server):
        thread = threading.Thread(target=server.serve_forever)
        thread.start()
        threads.append(thread)

    try:
        while 1:
            time.sleep(1)
    except:
        print('shutting down')
        for server in (syslog_server, dump_server):
            server.shutdown()
        for thread in threads:
            thread.join()

