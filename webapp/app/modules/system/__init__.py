from flask import Blueprint

module_bp = Blueprint(
    'system',
    __name__,
    template_folder='templates',
    static_folder='static',
    url_prefix='/system'
)

from . import routes