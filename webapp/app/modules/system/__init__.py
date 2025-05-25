from flask import Blueprint

system_bp = Blueprint(
    'system',
    __name__,
    template_folder='templates',
    static_folder='static',
    # url_prefix='/network'
)

# from . import routes