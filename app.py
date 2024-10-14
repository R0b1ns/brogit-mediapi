from app import app, socketio

if __name__ == '__main__':
    # app.run(debug=True)
    socketio.run(app, host="0.0.0.0", port=80, debug=True, allow_unsafe_werkzeug=True)