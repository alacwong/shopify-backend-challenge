from flask import Blueprint

bp_name = "images"
images_bp = Blueprint(bp_name, __name__, url_prefix="/images")