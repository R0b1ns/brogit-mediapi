from flask import Blueprint

module_bp = Blueprint(
    'gmrender-resurrect',
    __name__,
    template_folder='templates',
    static_folder='static',
    url_prefix='/gmrender-resurrect'
)

from . import routes