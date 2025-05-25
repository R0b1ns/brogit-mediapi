from flask import Blueprint

ethernet_bp = Blueprint(
    'ethernet',
    __name__,
    template_folder='templates',
    static_folder='static',
    # url_prefix='/network'
)

# from . import routes