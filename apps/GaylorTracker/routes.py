from flask import render_template, request, session, jsonify
from apps.auth.utils import login_required
from .models import get_all_gaylor, save_auditory_record,get_previous_audits
import smtplib
from email.message import EmailMessage
from email.message import EmailMessage
from datetime import datetime
import json, smtplib
from office365.runtime.auth.user_credential import UserCredential
from office365.sharepoint.client_context import ClientContext
import os
from . import gaylorTracker_bp  # Importar el Blueprint desde __init__.py


@gaylorTracker_bp.route('/', methods=['GET'])
@login_required
def index():
    usuario = session.get('usuario')
    filter_packing = request.args.get('packing_object')

    registros = []
    total_resultados = 0
    handling_units_unicas = 0
    auditorias_previas = []
    tiene_auditorias_previas = False

    if filter_packing:
        # Obtener datos del gaylord
        registros = get_all_gaylor(filter_packing=filter_packing)
        total_resultados = len(registros)
        handling_units_unicas = len(set(r['handling_unit'] for r in registros)) if registros else 0
        
        # Obtener auditorías previas
        auditorias_previas = get_previous_audits(filter_packing)
        tiene_auditorias_previas = len(auditorias_previas) > 0

    return render_template(
        'GaylorTrackerIndex.html',
        registros=registros,
        usuario=usuario,
        filter_packing=filter_packing,
        total_resultados=total_resultados,
        handling_units_unicas=handling_units_unicas,
        auditorias_previas=auditorias_previas,
        tiene_auditorias_previas=tiene_auditorias_previas
    )


@gaylorTracker_bp.route('/send_report', methods=['POST'])
@login_required
def send_report():


    try:
        usuario = session.get('usuario', 'Desconocido')
        subject = request.form.get('subject', 'Reporte sin asunto')
        body = request.form.get('body', '')
        excel_file = request.files.get('excel_file')
        over_hus = json.loads(request.form.get('over_hus', '[]'))
        short_hus = json.loads(request.form.get('short_hus', '[]'))
        hu_fisicos = request.form.get('huFisicos', '0')
        hu_sap = request.form.get('huRegistrados', '0')
        linea = request.form.get('linea', 'Desconocido')
        carrier = request.form.get('carrier', 'Desconocido')

        # Determinar tipo de hallazgo
        if over_hus and short_hus:
            tipo_hallazgo = "Over y Short"
        elif over_hus:
            tipo_hallazgo = "Over"
        elif short_hus:
            tipo_hallazgo = "Short"
        else:
            tipo_hallazgo = "Sin hallazgos"

        # Cuerpo final
        body_final = body
        body_final += f"\n\nAuditor: {usuario}\nLinea: {linea}\nCarrier: {carrier}"

        # Crear asunto con fecha
        fechaHora = datetime.now().strftime("%d/%m/%Y, %H:%M:%S")
        subject_final = f"{subject}"

        # Destinatarios de producción
        to_email = [
            # 'MXSystemsSupport@essilorusa.com',
            'Pcoverru@essilorluxottica.id',
            'QualityDC@essilorusa.com',
            'Customs-ELMTIJ@essilorluxottica.id',
            'juan.vazquez@essilorusa.com',
            'cesar.cortes@essilorluxottica.com',
            'Erika.Gonzalez@essilorluxottica.com'
            # 'johan.lozoya@essilorluxottica.id'
        ]

        # Crear correo
        msg = EmailMessage()
        msg['Subject'] = subject_final
        msg['From'] = 'johan.lozoya@essilorluxottica.id'
        msg['To'] = ', '.join(to_email)
        msg.set_content(body_final)

        # Adjuntar Excel
        if excel_file:
            msg.add_attachment(
                excel_file.read(),
                maintype='application',
                subtype='vnd.openxmlformats-officedocument.spreadsheetml.sheet',
                filename=excel_file.filename
            )

        # Enviar correo
        with smtplib.SMTP('smtp.office365.com', 587) as smtp:
            smtp.starttls()
            smtp.login('johan.lozoya@essilorluxottica.id', 'elpepeBot123!')
            smtp.send_message(msg)

        return jsonify({'message': f'Reporte enviado correctamente ({tipo_hallazgo}).'})

    except Exception as e:
        return jsonify({'message': f'Error inesperado: {str(e)}'}), 500









@gaylorTracker_bp.route('/save_audit', methods=['POST'])
@login_required
def save_audit():
    """
    Guarda un registro de auditoría en la API automáticamente
    """
    try:
        print("🔍 DEBUG: Entrando a /save_audit")
        usuario = session.get('usuario', 'Desconocido')
        print(f"🔍 DEBUG: Usuario: {usuario}")
        
        data = request.get_json()
        print(f"🔍 DEBUG: Datos recibidos: {data}")
        
        if not data:
            return jsonify({'message': 'No se recibieron datos', 'saved': False}), 400
        
        packing_object = data.get('packing_object')
        hu_fisicos = int(data.get('hu_fisicos', 0))
        over_count = int(data.get('over_count', 0))
        short_count = int(data.get('short_count', 0))
        
        print(f"🔍 DEBUG: Procesando - PO: {packing_object}, Físicos: {hu_fisicos}, Over: {over_count}, Short: {short_count}")
        
        # Calcular fecha y valores derivados
        current_date = datetime.now()
        year = current_date.year
        quarter = (current_date.month - 1) // 3 + 1
        week_number = current_date.isocalendar()[1]
        
        print(f"🔍 DEBUG: Fecha calculada - Año: {year}, Trimestre: {quarter}, Semana: {week_number}")
        
        # Guardar en la API de auditoría
        success = save_auditory_record(
            packing_object=packing_object,
            qty=hu_fisicos,
            auditor=usuario,
            over=over_count,
            short=short_count,
            dateTime=current_date.isoformat(),
            year=year,
            quarter=quarter,
            weekNumber=week_number
        )
        
        if success:
            print("✅ DEBUG: Auditoría guardada exitosamente")
            return jsonify({
                'message': f'Auditoría guardada correctamente',
                'saved': True
            })
        else:
            print("❌ DEBUG: Error al guardar en API")
            return jsonify({
                'message': 'Error al guardar en la base de datos de auditoría',
                'saved': False
            }), 500
            
    except Exception as e:
        print(f"❌ DEBUG: Excepción en save_audit: {str(e)}")
        return jsonify({
            'message': f'Error inesperado: {str(e)}',
            'saved': False
        }), 500
    
@gaylorTracker_bp.route('/dashboard')
@login_required
def dashboard():
    """
    Dashboard con gráficas de auditorías
    """
    usuario = session.get('usuario')
    
    # Obtener parámetros de filtro
    date_from = request.args.get('date_from', '')
    date_to = request.args.get('date_to', '')
    week_number = request.args.get('week_number', '')
    year = request.args.get('year', '')
    
    return render_template('gaylor_dashboard.html', 
                         usuario=usuario,
                         date_from=date_from,
                         date_to=date_to,
                         week_number=week_number,
                         year=year)