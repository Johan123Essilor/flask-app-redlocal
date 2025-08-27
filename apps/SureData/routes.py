from flask import render_template, request, session
from apps.auth.utils import login_required
from . import confirmationTracker_bp
from .models import get_by_confirmation

@confirmationTracker_bp.route('/', methods=['GET'])
# @login_required
def index():
    usuario = session.get('usuario')
    confirmation_nr = request.args.get('confirmation_nr')

    # Obtener todos los registros que coincidan con confirmation_nr
    registros = get_by_confirmation(confirmation_nr=confirmation_nr)
    
    # Contar solo los registros donde tote_ID != "NO-TOTE"
    total_resultados = len([r for r in registros if r.get("tote_ID") != "NO-TOTE"])

    return render_template(
        'ConfirmationIndex.html',
        registros=registros,
        usuario=usuario,
        confirmation_nr=confirmation_nr,
        total_resultados=total_resultados
    )
