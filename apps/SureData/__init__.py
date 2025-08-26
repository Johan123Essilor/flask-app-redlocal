from flask import Blueprint

confirmationTracker_bp = Blueprint(
    'confirmationTracker', __name__,
    template_folder='templates',
    static_folder='static'
)

from . import routes  # aquí importas tus rutas
