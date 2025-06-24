from flask import Blueprint

module_bp = Blueprint(
    'shairport-sync',
    __name__,
    template_folder='templates',
    static_folder='static',
    url_prefix='/shairport-sync'
)

from . import routes