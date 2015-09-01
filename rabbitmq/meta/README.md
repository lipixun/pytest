# The rabbitmq meta (properties attribute of a message)

Available keys

* persistent When set to true, RabbitMQ will persist message to disk.  
* mandatory This flag tells the server how to react if the message cannot be routed to a queue. If this flag is set to true, the server will return an unroutable message to the producer with a `basic.return` AMQP method. If this flag is set to false, the server silently drops the message.  
* timestamp Timestamp of the moment when message was sent, in seconds since the Epoch  
* expiration Message expiration specification as a string  
* type Message type as a string. Recommended to be used by applications instead of including this information into the message payload.  
* reply_to Commonly used to name a reply queue (or any other identifier that helps a consumer application to direct its response). Applications are encouraged to use this attribute instead of putting this information into the message payload.   
* content_type MIME content type of message payload. Has the same purpose/semantics as HTTP Content-Type header.  
* content_encoding MIME content encoding of message payload. Has the same purpose/semantics as HTTP Content-Encoding header.  
* correlation_id ID of the message that this message is a reply to. Applications are encouraged to use this attribute instead of putting this information into the message payload.   
* priority Message priority, from 0 to 9.  
* message_id Message identifier as a string. If applications need to identify messages, it is recommended that they use this attribute instead of putting it into the message payload.   
* user_id Sender's identifier. Note that RabbitMQ will check that the [value of this attribute is the same as username AMQP connection was authenticated with](http://www.rabbitmq.com/validated-user-id.html), it SHOULD NOT be used to transfer, for example, other application user ids or be used as a basis for some kind of Single Sign-On solution.   
* app_id Application identifier string, for example, "eventoverse" or "webcrawler"  
* application_headers The application headers should be placed here
