from flask import render_template, request, session, jsonify
from apps.auth.utils import login_required
from .models import get_all_gaylor
import smtplib
from email.message import EmailMessage
from . import gaylorTracker_bp  # Importar el Blueprint desde __init__.py

# Ruta principal para mostrar el tracker
@gaylorTracker_bp.route('/', methods=['GET'])
# @login_required  # Descomentar si se quiere proteger
def index():
    usuario = session.get('usuario')
    filter_packing = request.args.get('packing_object')

    registros = []
    total_resultados = 0
    handling_units_unicas = 0

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

# Ruta para enviar el reporte por correo
@gaylorTracker_bp.route('/send_report', methods=['POST'])
@login_required
def send_report():
    usuario = session.get('usuario', 'Desconocido')

    try:
        # Usamos request.form y request.files porque enviaremos FormData
        subject = request.form.get('subject', 'Reporte sin asunto')
        body = request.form.get('body', '')
        to_email = request.form.get('to', 'johan.lozoya@essilorluxottica.id')
        excel_file = request.files.get('excel_file')

        # Agregar nombre del auditor al cuerpo
        body += f"\n\nAuditor: {usuario}"

        # Crear el mensaje
        msg = EmailMessage()
        msg['Subject'] = subject
        msg['From'] = 'johan.lozoya@essilorluxottica.id'
        msg['To'] = to_email
        msg.set_content(body)

        # Adjuntar el Excel si existe
        if excel_file:
            msg.add_attachment(
                excel_file.read(),
                maintype='application',
                subtype='vnd.openxmlformats-officedocument.spreadsheetml.sheet',
                filename=excel_file.filename
            )

        # Configuración SMTP
        with smtplib.SMTP('smtp.office365.com', 587) as smtp:
            smtp.starttls()
            smtp.login('johan.lozoya@essilorluxottica.id', 'Tiernoperogangsta!')
            smtp.send_message(msg)

        return jsonify({'message': 'Reporte enviado con Excel adjunto correctamente.'})
    
    except smtplib.SMTPAuthenticationError:
        return jsonify({'message': 'Error de autenticación SMTP. Verifica las credenciales.'}), 500
    except smtplib.SMTPException as e:
        return jsonify({'message': f'Error SMTP: {str(e)}'}), 500
    except Exception as e:
        return jsonify({'message': f'Error inesperado: {str(e)}'}), 500