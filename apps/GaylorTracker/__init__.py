from flask import Blueprint, render_template, request, session, flash
from apps.auth.utils import login_required
from .models import get_all_gaylor

gaylorTracker_bp = Blueprint(
    'gaylorTracker', __name__,
    template_folder='templates',
    static_folder='static'
)

@gaylorTracker_bp.route('/', methods=['GET'])
# @login_required
def index():
    usuario = session.get('usuario')
    filter_packing = request.args.get('packing_object')

    registros = []
    total_resultados = 0
    handling_units_unicas = 0

    # Solo obtener registros si se pasó un filtro
    if filter_packing:
        registros = get_all_gaylor(filter_packing=filter_packing)
        total_resultados = len(registros)
        handling_units_unicas = len(set(r['handling_unit'] for r in registros)) if registros else 0

    return render_template(
        'GaylorTrackerIndex.html',
        registros=registros,
        usuario=usuario,
        filter_packing=filter_packing,
        total_resultados=total_resultados,
        handling_units_unicas=handling_units_unicas
    )
