import socket
import time

from flask import Flask, render_template, session, request, jsonify
from flask_cors import CORS
from flask_socketio import SocketIO, emit

from app.lib.wifi import scan_wifi, connect_to_wifi

app = Flask(__name__)
app.secret_key = 'your_secret_key'
socketio = SocketIO(app)
CORS(app, resources={r"/": {"origins": "*"}})


@app.route('/')
def index():
    return render_template('index.html', hostname="http://{}".format(socket.gethostname()))


@socketio.on('request_wifi')
def handle_request_wifi():
    networks = scan_wifi()
    emit('response_wifi', {'networks': networks})


@app.route('/api/connect', methods=['GET'])
def connect_to_network():
    ssid = request.args.get('ssid')
    password = request.args.get('password')

    time.sleep(6)

    if not ssid:
        return jsonify({"error": "SSID is required"}), 400

    try:
        connect_to_wifi(ssid, password)
        return jsonify({"message": f"Connected to {ssid}"}), 200
    except Exception as e:
        return jsonify({"message": str(e)}), 500


if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=80, debug=True, allow_unsafe_werkzeug=True)
