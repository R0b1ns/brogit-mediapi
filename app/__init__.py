from flask import Flask, render_template, session
from flask_socketio import SocketIO, emit

from app.lib.wifi import scan_wifi

app = Flask(__name__)
app.secret_key = 'your_secret_key'
socketio = SocketIO(app)



@app.route('/')
def index():
    return render_template('index.html')


@socketio.on('request_wifi')
def handle_request_wifi():
    networks = scan_wifi()
    emit('response_wifi', {'networks': networks})

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=80, debug=True, allow_unsafe_werkzeug=True)
