from flask import Blueprint

usb_bp = Blueprint(
    'usb',
    __name__,
    template_folder='templates',
    static_folder='static',
    # url_prefix='/network'
)

# from . import routes