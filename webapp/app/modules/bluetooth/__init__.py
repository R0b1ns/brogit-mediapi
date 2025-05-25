from flask import Blueprint

bluetooth_bp = Blueprint(
    'bluetooth',
    __name__,
    template_folder='templates',
    static_folder='static',
    # url_prefix='/network'
)

# from . import routes