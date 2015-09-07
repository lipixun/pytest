#!/usr/bin/env python
# encoding=utf8
# The dead channel applicationn

import sys
reload(sys)
sys.setdefaultencoding('utf8')

from uuid import uuid4
from time import time, sleep

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
        result = self._channel.queue.declare(arguments = { 'x-dead-letter-exchange': 'amq.topic', 'x-dead-letter-routing-key': 'test.dead_channel' })
        self._deadQueue = result[0]
        # Send a message
        self._channel.basic.publish(Message('OMG! I\'m dead!'), '', self._deadQueue)

    def dead(self):
        """Normal dead
        """
        self._channel.close()

if __name__ == '__main__':

    from argparse import ArgumentParser

    def getArguments():
        """Get arguments
        """
        parser = ArgumentParser(description = 'RabbitMQ dead channel client')
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
        # Go to dead
        print 'Will go to dead in 10s, or you can use ctrl + c to cause a unexpected death'
        sleep(10)
        client.dead()
        print 'Normal dead'

    main()

