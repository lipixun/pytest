#!/usr/bin/env python
# encoding=utf8
# The RPC server

import sys
reload(sys)
sys.setdefaultencoding('utf8')

from haigha.connections.rabbit_connection import RabbitConnection
from haigha.message import Message

class Server(object):
    """The RPC Server
    """
    def __init__(self, host, port, vhost, user, password):
        """Create a new Server
        """
        self._conn = RabbitConnection(host = host, port = port, vhost = vhost, user = user, password = password)
        self._channel = self._conn.channel()
        self._channel.queue.declare('test_rpc', auto_delete = True)
        self._channel.basic.consume('test_rpc', self.callee, no_ack = False)

    def run(self):
        """Waiting for response
        """
        while True:
            self._conn.read_frames()

    def callee(self, message):
        """The callee method
        """
        num = int(message.body)
        replyTo = message.properties.get('reply_to')
        correlationID = message.properties.get('correlation_id')
        deliveryTag = message.delivery_info.get('delivery_tag')
        # Print the meta
        print 'Receive message body [%s] replyTo [%s] correlationID [%s]' % (num, replyTo, correlationID)
        # Return add 1
        self._channel.basic.publish(Message(str(num + 1), correlation_id = correlationID), '', replyTo)
        # ACK
        self._channel.basic.ack(deliveryTag)

if __name__ == '__main__':

    from argparse import ArgumentParser

    def getArguments():
        """Get arguments
        """
        parser = ArgumentParser(description = 'RPC test server')
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
        server.run()

    main()

