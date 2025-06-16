from flask import Blueprint, request, abort

api_bp = Blueprint('api', __name__, url_prefix='/api')

@api_bp.before_request
def enforce_json():
    if request.method in ("POST", "PUT", "PATCH"):
        if not request.is_json:
            abort(400, description="JSON expected")


from . import settings
