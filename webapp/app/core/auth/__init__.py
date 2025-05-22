from flask import Blueprint

# Auth Blueprint
auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

from . import routes