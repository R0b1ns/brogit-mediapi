from flask import Blueprint

network_bp = Blueprint(
    'network',
    __name__,
    template_folder='templates',
    static_folder='static',
    url_prefix='/network'
)

# from . import routes