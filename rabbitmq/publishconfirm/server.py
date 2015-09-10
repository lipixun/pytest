#!/usr/bin/env python
# encoding=utf8
# The publish confirm test server

import sys
reload(sys)
sys.setdefaultencoding('utf8')

import gevent
from gevent import monkey
monkey.patch_all()

from haigha.connections.rabbit_connection import RabbitConnection
from haigha.message import Message

class Server(object):
    """The Meta Server
    """
    def __init__(self, host, port, vhost, user, password):
        """Create a new Server
        """
        self._conn = RabbitConnection(transport = 'gevent', host = host, port = port, vhost = vhost, user = user, password = password)
        gevent.spawn(self.loop)
        self._channel = self._conn.channel()
        self._channel.basic.qos(prefetch_count = 10)
        self._channel.queue.declare('test_confirm', auto_delete = True)
        self._channel.basic.consume('test_confirm', self.callback, no_ack = False)

    def loop(self):
        """Waiting for response
        """
        while self._conn:
            self._conn.read_frames()
            gevent.sleep()

    def callback(self, message):
        """The callee method
        """
        # NOTE:
        #   Here, we have to spawn the actually message processing method in order to process the message parallely
        gevent.spawn(self.process, message)

    def process(self, message):
        """Process the message
        """
        body = message.body
        deliveryInfo = message.delivery_info
        deliveryTag = deliveryInfo.get('delivery_tag')
        # Print the meta
        print 'Receive message body [%s] deliveryTag [%s], will sleep 10s' % (body, deliveryTag)
        gevent.sleep(10)
        # ACK
        print 'Wake up, ACK the message'
        self._channel.basic.ack(deliveryTag)

if __name__ == '__main__':

    from argparse import ArgumentParser

    def getArguments():
        """Get arguments
        """
        parser = ArgumentParser(description = 'Confirm test server')
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
        server = Server(args.host, args.port, args.vhost, args.user, args.password)
        gevent.sleep(1000000)

    main()

