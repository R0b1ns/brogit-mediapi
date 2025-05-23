from flask import Blueprint

# Main Blueprint
main_bp = Blueprint('main', __name__)

from . import routes
