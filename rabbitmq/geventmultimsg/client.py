#!/usr/bin/env python
# encoding=utf8
# The gevent test client

import sys
reload(sys)
sys.setdefaultencoding('utf8')

import gevent
from gevent import monkey
monkey.patch_all()

from haigha.connections.rabbit_connection import RabbitConnection
from haigha.message import Message

class Client(object):
    """The RPC Client
    """
    def __init__(self, host, port, vhost, user, password):
        """Create a new Server
        """
        self._conn = RabbitConnection(transport = 'gevent', host = host, port = port, vhost = vhost, user = user, password = password)
        gevent.spawn(self.loop)
        self._channel = self._conn.channel()

    def loop(self):
        """The loop
        """
        while self._conn:
            self._conn.read_frames()
            gevent.sleep()

    def call(self):
        """The call method
        """
        self._channel.basic.publish(Message('A test body'), '', 'test_gevent')

if __name__ == '__main__':

    from argparse import ArgumentParser

    def getArguments():
        """Get arguments
        """
        parser = ArgumentParser(description = 'Gevent test client')
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
        for i in range(0, 50):
            print 'Send message'
            client.call()
            gevent.sleep(0.1)
        # Done
        print 'Done'
        gevent.sleep(1000)

    main()

