from flask import Blueprint

module_bp = Blueprint(
    'bluetooth',
    __name__,
    template_folder='templates',
    static_folder='static',
    url_prefix='/bluetooth'
)

from . import routes