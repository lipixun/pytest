#!/usr/bin/env python
# encoding=utf8
# The inspector will consume all events

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
        self._channel.queue.declare('test_event', auto_delete = True)
        self._channel.queue.bind('test_event', exchange = 'amq.rabbitmq.event', routing_key = '#')
        self._channel.basic.consume('test_event', self.callback, no_ack = False)

    def run(self):
        """Waiting for response
        """
        while True:
            self._conn.read_frames()

    def callback(self, message):
        """The callee method
        """
        body = message.body
        eventType = message.delivery_info.get('routing_key')
        deliveryTag = message.delivery_info.get('delivery_tag')
        # Print the meta
        print 'Event [%s] message body [%s] headers [%s] deliveryInfo [%s]' % (eventType, body, message.properties, message.delivery_info)
        # ACK
        self._channel.basic.ack(deliveryTag)

if __name__ == '__main__':

    from argparse import ArgumentParser

    def getArguments():
        """Get arguments
        """
        parser = ArgumentParser(description = 'RabbitMQ event inspector')
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
        # Create the inspector
        inspector = Inspector(args.host, args.port, args.vhost, args.user, args.password)
        inspector.run()

    main()

