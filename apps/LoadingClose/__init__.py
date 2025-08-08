from flask import Blueprint
from .models import init_db
init_db()

ShippingClose_bp = Blueprint(
    'ShippingClose',
    __name__,
    template_folder='templates',
    static_folder='static',
    static_url_path='/ShippingClose/static'
)

from . import routes  # <- Esto debe estar al final
