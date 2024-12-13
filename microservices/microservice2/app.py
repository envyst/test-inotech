from flask import Flask, request, jsonify
import socket
try:
    import json
except ImportError:
    import simplejson as json
    
logserver_ip = 'logstash'
logserver_port = 5044

app = Flask(__name__)

@app.route('/log', methods=['GET'])
def log_message():
    msg = request.args.get('msg', 'No message provided')
    log_data = {
        "level": "INFO",
        "service": "microservice2",
        "message": msg,
        "host": socket.gethostname()
    }
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((logserver_ip, logserver_port))

    # Correctly encode the message as bytes
    s.send((json.dumps(log_data) + '\n').encode('utf-8'))
    s.close()
    return jsonify({"message": msg})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002)
