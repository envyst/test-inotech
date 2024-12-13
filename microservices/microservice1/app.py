from flask import Flask, jsonify
import socket
try:
    import json
except ImportError:
    import simplejson as json
    
logserver_ip = 'logstash'
logserver_port = 5044

app = Flask(__name__)

@app.route('/')
def hello_world():
    response = "Hello, World"
    log_data = {
        "level": "INFO",
        "service": "microservice1",
        "message": response,
        "host": socket.gethostname()
    }
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((logserver_ip, logserver_port))

    # Correctly encode the message as bytes
    s.send((json.dumps(log_data) + '\n').encode('utf-8'))
    s.close()
    return jsonify({"message": response})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
