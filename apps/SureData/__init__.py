from flask import Blueprint
from .models import init_db

confirmationTracker_bp = Blueprint(
    'confirmationTracker', __name__,
    template_folder='templates',
    static_folder='static'
)

# 🔹 Crear la tabla al iniciar el blueprint
init_db()

from . import routes
