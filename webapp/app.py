from app import create_app

app, socketio = create_app()

# TODO: Look if you need that in the future
# def deploy():
#     """Run deployment tasks."""
#     from app import create_app,db
#     from flask_migrate import upgrade,migrate,init,stamp
#     from models import User
#
#     app = create_app()
#     app.app_context().push()
#     db.create_all()
#
#     # migrate database to latest revision
#     init()
#     stamp()
#     migrate()
#     upgrade()
#
# deploy()


if __name__ == '__main__':
    # app.run(debug=True, host="0.0.0.0", port=80)
    socketio.run(app, host="0.0.0.0", port=80, debug=True, allow_unsafe_werkzeug=True)