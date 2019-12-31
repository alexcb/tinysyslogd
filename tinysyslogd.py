#!/usr/bin/env python3

LISTEN_HOST = "0.0.0.0"
LISTEN_PORT = 514

import socketserver

class SyslogHandler(socketserver.BaseRequestHandler):

    def handle(self):
        client = str(self.client_address)
        msg = str(self.request[0].strip())
        print(f'{client}: {msg}')

if __name__ == "__main__":
    server = socketserver.UDPServer((LISTEN_HOST,LISTEN_PORT), SyslogHandler)
    server.serve_forever()
