from flask import Blueprint
from .models import init_users
init_users()

auth_bp = Blueprint(
    'auth',
    __name__,
    template_folder='templates'
)

from . import routes
