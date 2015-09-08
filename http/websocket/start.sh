#!/bin/bash
# Start the server

uwsgi --http :18910 --http-websockets --wsgi-file uwsgiserver.py --gevent 10 --processes 1 --need-app --lazy

