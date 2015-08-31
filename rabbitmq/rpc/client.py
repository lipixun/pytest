#!/usr/bin/env python
# encoding=utf8
# The RPC client

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
        result = self._channel.queue.declare(exclusive = True)
        self._callbackQueue = result[0]
        self._channel.basic.consume(self._callbackQueue, self.onResponse, no_ack = True)
        self._response = None

    def onResponse(self, message):
        """On response
        """
        correlationID = message.properties.get('correlation_id')
        print 'Receive server response [%s] correlationID [%s]' % (message.body, correlationID)
        self._response = int(message.body)

    def call(self, number):
        """The call method
        """
        self._response = None
        corrID = str(uuid4())
        print 'Call server with request [%s] correlationID [%s]' % (number, corrID)
        self._channel.basic.publish(Message(str(number), reply_to = self._callbackQueue, correlation_id = corrID), '', 'test_rpc')
        while self._response is None:
            self._conn.read_frames()
        # Done
        return self._response

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
        while True:
            try:
                print 'Input>>',
                number = raw_input()
                if not number.isdigit():
                    print 'Please input a number, try again'
                    continue
                t1 = time()
                result = client.call(number)
                t2 = time()
                print 'Server return [%s] in [%.4fms]' % (result, t2 - t1)
            except EOFError:
                break

    main()

