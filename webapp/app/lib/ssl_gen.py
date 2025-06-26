import datetime
import tempfile

from cryptography import x509
from cryptography.x509.oid import NameOID
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import rsa

def generate_self_signed_cert():
    key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    subject = x509.Name([
        x509.NameAttribute(NameOID.COMMON_NAME, u'localhost'),
    ])
    cert = (
        x509.CertificateBuilder()
        .subject_name(subject)
        .issuer_name(subject)
        .public_key(key.public_key())
        .serial_number(x509.random_serial_number())
        .not_valid_before(datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(days=1))
        .not_valid_after(datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(days=30))
        .sign(key, hashes.SHA256())
    )

    cert_pem = cert.public_bytes(serialization.Encoding.PEM)
    key_pem = key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.TraditionalOpenSSL,
        encryption_algorithm=serialization.NoEncryption(),
    )

    cert_file = tempfile.NamedTemporaryFile(delete=False, suffix='.pem')
    key_file = tempfile.NamedTemporaryFile(delete=False, suffix='.pem')
    cert_file.write(cert_pem)
    key_file.write(key_pem)
    cert_file.close()
    key_file.close()
    return cert_file.name, key_file.name

if __name__ == '__main__':
    cert_path = 'cert.pem'
    key_path = 'key.pem'

    if os.path.exists(cert_path) and os.path.exists(key_path):
        ssl_ctx = (cert_path, key_path)
    else:
        ssl_ctx = generate_self_signed_cert()

    socketio.run(app, host='0.0.0.0', port=443, ssl_context=ssl_ctx)
