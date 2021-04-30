from flask import Blueprint

bp_name = "image_view"
images_bp = Blueprint(bp_name, __name__, url_prefix="/images")
