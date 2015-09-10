#!/usr/bin/env python
# encoding=utf8
# The publish confirm test client

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
        self._channel.confirm.select()
        self._channel.basic.set_return_listener(self.onBasicReturn)
        self._channel.basic.set_ack_listener(self.onDeliverAck)
        self._channel.basic.set_nack_listener(self.onDeliverNAck)

    def loop(self):
        """The loop
        """
        while self._conn:
            self._conn.read_frames()
            gevent.sleep()

    def onBasicReturn(self, message):
        """On basic return
        """
        print 'Basic return message [%s]' % message

    def onDeliverAck(self, messageID):
        """On deliver ACK
        """
        print 'Deliver ACK [%s]' % messageID

    def onDeliverNAck(self, messageID, requeue):
        """On deliver nack
        """
        print 'Deliver NACK [%s] Requeue [%s]' % (messageID, requeue)

    def call(self, content, queue):
        """The call method
        """
        return self._channel.basic.publish(Message(content), '', queue)

if __name__ == '__main__':

    from argparse import ArgumentParser

    def getArguments():
        """Get arguments
        """
        parser = ArgumentParser(description = 'Confirm test client')
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
        # Send the messages
        msgID = client.call('A good message', 'test_confirm')
        print 'Sent good message [%s]' % msgID
        msgID = client.call('A bad message', 'a_none_existed_queue')
        print 'Sent bad message [%s]' % msgID
        print 'Wait for deliver ack / nack'
        # Done
        gevent.sleep(1000)

    main()

