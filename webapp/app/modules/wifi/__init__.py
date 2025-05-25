from flask import Blueprint

wifi_bp = Blueprint(
    'wifi',
    __name__,
    template_folder='templates',
    static_folder='static',
    # url_prefix='/network'
)

# from . import routes