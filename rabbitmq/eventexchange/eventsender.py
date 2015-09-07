#!/usr/bin/env python
# encoding=utf8
# The rabbitMQ event sender

import sys
reload(sys)
sys.setdefaultencoding('utf8')

import os
import socket

from uuid import uuid4
from time import time, sleep

from haigha.connections.rabbit_connection import RabbitConnection
from haigha.message import Message

class EventSender(object):
    """The event sender
    """
    def __init__(self, host, port, vhost, user, password):
        """Create a new EventSender
        """
        self._conn = RabbitConnection(host = host, port = port, vhost = vhost, user = user, password = password)
        self._channel = self._conn.channel()
        self._channel.queue.declare('_aprefix/%s/webservice/%s' % (socket.gethostname(), os.getpid()), exclusive = True)

if __name__ == '__main__':

    from argparse import ArgumentParser

    def getArguments():
        """Get arguments
        """
        parser = ArgumentParser(description = 'RabbitMQ event sender')
        parser.add_argument('--host', dest = 'host', required = True, help = 'The host')
        parser.add_argument('--port', dest = 'port', default = 5672, type = int, help = 'The port')
        parser.add_argument('--vhost', dest = 'vhost', default = '/', help = 'The virtual host')
        parser.add_argument('--user', dest = 'user', default = 'test', help = 'The user name')
        parser.add_argument('--password', dest = 'password', default = 'test', help = 'The password')
        # Done
        return parser.parse_args()

    def main():
        """The main entry
        """
        args = getArguments()
        # Create the server
        sender = EventSender(args.host, args.port, args.vhost, args.user, args.password)

    main()

