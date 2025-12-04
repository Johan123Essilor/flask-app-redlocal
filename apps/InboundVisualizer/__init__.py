from flask import Blueprint

# Definir el Blueprint
inboundVisualizer_bp = Blueprint(
    'inboundVisualizer', __name__,
    template_folder='templates',
    static_folder='static'
)

# Importar rutas (para registrarlas en el Blueprint)
from . import routes
