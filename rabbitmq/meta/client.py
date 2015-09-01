#!/usr/bin/env python
# encoding=utf8
# The Meta Test Client

import sys
reload(sys)
sys.setdefaultencoding('utf8')

from uuid import uuid4
from time import time

from haigha.connections.rabbit_connection import RabbitConnection
from haigha.message import Message

class Client(object):
    """The RPC Client
    """
    def __init__(self, host, port, vhost, user, password):
        """Create a new Server
        """
        self._conn = RabbitConnection(host = host, port = port, vhost = vhost, user = user, password = password)
        self._channel = self._conn.channel()

    def call(self):
        """The call method
        """
        self._channel.basic.publish(Message('A test body', correlation_id = '123', application_headers = { 'custom_header': 'value', 'custom_header1': 1 }), '', 'test_meta')

if __name__ == '__main__':

    from argparse import ArgumentParser

    def getArguments():
        """Get arguments
        """
        parser = ArgumentParser(description = 'RPC test client')
        parser.add_argument('--host', dest = 'host', required = True, help = 'The host')
        parser.add_argument('--port', dest = 'port', default = 5672, type = int, help = 'The port')
        parser.add_argument('--vhost', dest = 'vhost', default = '/test', help = 'The virtual host')
        parser.add_argument('--user', dest = 'user', default = 'test', help = 'The user name')
        parser.add_argument('--password', dest = 'password', default = 'test', help = 'The password')
        # Done
        return parser.parse_args()

    def main():
        """The main entry
        """
        args = getArguments()
        # Create the server
        client = Client(args.host, args.port, args.vhost, args.user, args.password)
        client.call()

    main()

