from flask import Blueprint

module_bp = Blueprint(
    'ethernet',
    __name__,
    template_folder='templates',
    static_folder='static',
    url_prefix='/ethernet'
)

from . import routes