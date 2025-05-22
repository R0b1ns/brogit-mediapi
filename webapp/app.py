from app import create_app

app, socketio = create_app()

if __name__ == '__main__':
    # app.run(debug=True, host="0.0.0.0", port=80)
    socketio.run(app, host="0.0.0.0", port=80, debug=True, allow_unsafe_werkzeug=True)