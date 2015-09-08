# encoding=utf8
# The web socket server by uwsgi
# NOTE:
#   The most part of the codes comes from uwsgi python websocket demo: https://github.com/unbit/uwsgi/blob/master/tests/websockets_echo.py

"""The websocket test
"""

import sys
reload(sys)
sys.setdefaultencoding('utf8')

import gevent
from gevent import monkey
monkey.patch_all()

import uwsgi
import time

def application(env, sr):
    """The main entry
    """
    # Get websocket scheme
    wsScheme = 'ws'
    if 'HTTPS' in env or env['wsgi.url_scheme'] == 'https':
        wsScheme = 'wss'
    # The path info
    if env['PATH_INFO'] == '/':
        sr('200 OK', [ ('Content-Type', 'text/html' ) ])
        return """
    <html>
      <head>
          <script language="Javascript">
            var s = new WebSocket("%s://%s/foobar/");
            s.onopen = function() {
              alert("connected !!!");
              s.send("ciao");
            };
            s.onmessage = function(e) {
        var bb = document.getElementById('blackboard')
        var html = bb.innerHTML;
        bb.innerHTML = html + '<br/>' + e.data;
            };
        s.onerror = function(e) {
            alert(e);
        }
    s.onclose = function(e) {
        alert("connection closed");
    }
            function invia() {
              var value = document.getElementById('testo').value;
              s.send(value);
            }
          </script>
     </head>
    <body>
        <h1>WebSocket</h1>
        <input type="text" id="testo"/>
        <input type="button" value="invia" onClick="invia();"/>
    <div id="blackboard" style="width:640px;height:480px;background-color:black;color:white;border: solid 2px red;overflow:auto">
    </div>
    </body>
    </html>
        """ % (wsScheme, env['HTTP_HOST'])

    elif env['PATH_INFO'] == '/foobar/':
        uwsgi.websocket_handshake()
        print 'Start a web socket connection'
        while True:
            msg = uwsgi.websocket_recv()
            uwsgi.websocket_send("Server receive [%s] %s" % (time.time(), msg))
        print 'Close a web socket connection'
