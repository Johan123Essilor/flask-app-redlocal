from flask import Blueprint
from .models import init_db
init_db()

SOPSite_bp = Blueprint(
    'SOPSite',
    __name__,
    template_folder='templates',
    static_folder='static',
    static_url_path='/SOPSite/static'
)

from . import routes  # <- Esto debe estar al final
