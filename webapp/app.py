import os
import ssl

from app import create_app
from app.lib.ssl_gen import generate_self_signed_cert

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
    cert_path = app.config['SSL_CERT_PATH'] if 'SSL_CERT_PATH' in app.config else ''
    key_path = app.config['SSL_KEY_PATH'] if 'SSL_KEY_PATH' in app.config else ''

    if os.path.exists(cert_path) and os.path.exists(key_path):
        ssl_ctx = (cert_path, key_path)
    else:
        ssl_ctx = generate_self_signed_cert()

    context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    context.load_cert_chain(certfile=ssl_ctx[0], keyfile=ssl_ctx[1])

    app.ssl_context = context  # Store reference for reloads

    socketio.run(
        app,
        host=app.config['HOST'] if 'HOST' in app.config else '127.0.0.1',
        port=int(app.config['PORT']) if 'PORT' in app.config else 5000,
        ssl_context=app.ssl_context if app.config['SSL_ENABLED'] else None,
        # debug = True,
        # allow_unsafe_werkzeug = True
    )