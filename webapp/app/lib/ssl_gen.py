import datetime
import logging
import os
import ssl
import tempfile
from typing import Tuple, Optional

from cryptography import x509
from cryptography.hazmat.backends import default_backend
from cryptography.x509.oid import NameOID
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from flask import Flask


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

def validate_certificate_pem(cert_pem: str) -> bool:
    cert = x509.load_pem_x509_certificate(cert_pem.encode(), default_backend())

    now = datetime.datetime.now(datetime.timezone.utc)
    if cert.not_valid_after < now:
        return False
    if cert.not_valid_before > now:
        return False

    # Optional: further checks like issuer, SANs, etc.

    return True

def validate_private_key_pem(key_pem: str, password: str = None) -> bool:
    serialization.load_pem_private_key(
        key_pem.encode(),
        password=password,
        backend=default_backend()
    )
    return True

# TODO: Rewrite that dirty code. Care of try except cases to elevate message to settings
def validate_and_update_ssl_certificate(publickey: str, privatekey: str, cert_path: str, key_path: str) -> tuple[bool, str]:
    # Step 1: Validate certificate content (expiry etc)
    valid, msg = validate_certificate_pem(publickey)
    if not valid:
        return False, msg

    # Step 2: Write cert and key temporarily to validate pair by loading SSL context
    try:
        with tempfile.NamedTemporaryFile('w+', delete=False) as tmp_cert, \
             tempfile.NamedTemporaryFile('w+', delete=False) as tmp_key:
            tmp_cert.write(publickey)
            tmp_key.write(privatekey)
            tmp_cert_path = tmp_cert.name
            tmp_key_path = tmp_key.name

        test_context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
        test_context.load_cert_chain(certfile=tmp_cert_path, keyfile=tmp_key_path)

    except Exception as e:
        return False, f"Invalid certificate or key: {str(e)}"

    finally:
        if 'tmp_cert_path' in locals() and os.path.exists(tmp_cert_path):
            os.remove(tmp_cert_path)
        if 'tmp_key_path' in locals() and os.path.exists(tmp_key_path):
            os.remove(tmp_key_path)

    # Step 3: Overwrite actual cert and key files
    try:
        with open(cert_path, 'w') as cert_file:
            cert_file.write(publickey)
        with open(key_path, 'w') as key_file:
            key_file.write(privatekey)
    except Exception as e:
        return False, f"Failed to write certificate or key: {str(e)}"

    return True, "Certificate updated successfully"


def reload_ssl_context(app: Flask, cert_path: str, key_path: str) -> Tuple[bool, Optional[str]]:
    try:
        with open(cert_path, 'r') as f:
            cert_pem = f.read()
        with open(key_path, 'r') as f:
            key_pem = f.read()
    except Exception as e:
        return False, f"Failed to read certificate or key files: {e}"

    # Validate certificate PEM (including expiry)
    valid, err = validate_certificate_pem(cert_pem)
    if not valid:
        return False, err

    # Validate private key PEM
    valid, err = validate_private_key_pem(key_pem)
    if not valid:
        return False, err

    # Final test: load SSLContext (pair validation)
    try:
        new_context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
        new_context.load_cert_chain(certfile=cert_path, keyfile=key_path)
    except Exception as e:
        return False, f"Failed to load SSL context: {e}"

    # Apply new SSL context
    try:
        app.ssl_context = new_context
        socketio = getattr(app, 'socketio_instance', None)
        if socketio and hasattr(socketio, 'server') and hasattr(socketio.server, 'ssl_context'):
            socketio.server.ssl_context = new_context
        return True, None
    except Exception as e:
        return False, f"Failed to apply SSL context: {e}"
