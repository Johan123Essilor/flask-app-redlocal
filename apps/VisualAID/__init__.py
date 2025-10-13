from flask import Blueprint
from .models import init_db

VisualAID_bp = Blueprint(
    'VisualAID', __name__,
    template_folder='templates',
    static_folder='static',
    static_url_path='/VisualAID/static'
)

init_db()

from . import routes
