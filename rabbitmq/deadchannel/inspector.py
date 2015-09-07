#!/usr/bin/env python
# encoding=utf8
# The inspector that will consume the channel dead message

import sys
reload(sys)
sys.setdefaultencoding('utf8')

from haigha.connections.rabbit_connection import RabbitConnection
from haigha.message import Message

class Inspector(object):
    """The Meta Server
    """
    def __init__(self, host, port, vhost, user, password):
        """Create a new Server
        """
        self._conn = RabbitConnection(host = host, port = port, vhost = vhost, user = user, password = password)
        self._channel = self._conn.channel()
        self._channel.queue.declare('test_dead_channel', auto_delete = True)
        self._channel.queue.bind('test_dead_channel', exchange = 'amq.topic', routing_key = 'test.dead_channel')
        self._channel.basic.consume('test_dead_channel', self.callback, no_ack = False)

    def run(self):
        """Waiting for response
        """
        while True:
            self._conn.read_frames()

    def callback(self, message):
        """The callee method
        """
        body = message.body
        deliveryInfo = message.delivery_info
        # Print body
        print 'Receive dead message [%s]' % body
        # ACK
        deliveryTag = deliveryInfo.get('delivery_tag')
        self._channel.basic.ack(deliveryTag)

if __name__ == '__main__':

    from argparse import ArgumentParser

    def getArguments():
        """Get arguments
        """
        parser = ArgumentParser(description = 'RabbitMQ dead channel inspector')
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
        # Create the inspector
        inspector = Inspector(args.host, args.port, args.vhost, args.user, args.password)
        inspector.run()

    main()

