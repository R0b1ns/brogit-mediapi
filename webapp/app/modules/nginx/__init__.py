from flask import Blueprint

module_bp = Blueprint(
    'nginx',
    __name__,
    template_folder='templates',
    static_folder='static',
    url_prefix='/nginx'
)

# from . import routes