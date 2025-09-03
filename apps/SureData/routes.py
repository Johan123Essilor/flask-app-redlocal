from flask import render_template, request, session, jsonify
from apps.auth.utils import login_required
from . import confirmationTracker_bp
from .models import get_by_confirmation, insert_summary

@confirmationTracker_bp.route('/', methods=['GET'])
# @login_required
def index():
    usuario = session.get('usuario')
    confirmation_nr = request.args.get('confirmation_nr', '').strip()

    registros = []
    total_resultados = 0

    if confirmation_nr:  
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


# 🔹 Ruta para guardar el resumen de escaneo en SQLite puro
@confirmationTracker_bp.route('/save_summary', methods=['POST'])
def save_summary():
    data = request.get_json()
    if not data:
        return jsonify({"status":"error","msg":"No se recibió data"}), 400

    try:
        resumen_id = insert_summary(
            confirmation_nr = data.get("confirmation_nr"),
            bin_Id = data.get("bin_Id"),   # 👈 nuevo campo
            total_hus = data.get("total_hus", 0),
            encontrados = data.get("encontrados", 0),
            overs = data.get("overs", 0),
            shorts = data.get("shorts", 0)
        )


        return jsonify({"status":"ok", "id": resumen_id})

    except Exception as e:
        import traceback
        print(traceback.format_exc())
        return jsonify({"status":"error", "msg": str(e)}), 500
