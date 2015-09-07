# [Failed]The rabbitmq dead channel

This test code indents to implement a 'dead channel message' which a message will be sent when the channel is closed (Normally or by accident)

Since rabbitmq doesn't support such feature as present (2015/09/07), I choose to use a dead letter to simulate dead channel

RabbitMQ doesn't implement dead letter of deleted queue, so, there's no way to do so
