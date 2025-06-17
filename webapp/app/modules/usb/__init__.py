from flask import Blueprint

module_bp = Blueprint(
    'usb',
    __name__,
    template_folder='templates',
    static_folder='static',
    url_prefix='/usb'
)

from . import routes