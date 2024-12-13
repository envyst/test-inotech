# !/usr/bin/python

import socket
try:
    import json
except ImportError:
    import simplejson as json

logserver_ip = 'localhost'
logserver_port = 5044
json_message = {}

json_message['message'] = 'Test'
json_message['sourcetype'] = 'microservice'
json_message['level'] = 'INFO'

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((logserver_ip, logserver_port))

# Correctly encode the message as bytes
s.send((json.dumps(json_message) + '\n').encode('utf-8'))
s.close()
