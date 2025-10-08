from flask import render_template, request, session, jsonify
from apps.auth.utils import login_required
from .models import get_all_gaylor
import smtplib
from email.message import EmailMessage
from . import gaylorTracker_bp  # Importar el Blueprint desde __init__.py

# Ruta principal para mostrar el tracker
@gaylorTracker_bp.route('/', methods=['GET'])
@login_required  # Descomentar si se quiere proteger
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

@gaylorTracker_bp.route('/send_report', methods=['POST'])
@login_required
def send_report():
    usuario = session.get('usuario', 'Desconocido')

    try:
        subject = request.form.get('subject', 'Reporte sin asunto')
        body = request.form.get('body', '')
        excel_file = request.files.get('excel_file')

        # Agregar auditor al cuerpo del mensaje
        body += f"\n\nAuditor: {usuario}"

        # Destinatario fijo
        to_email = ['MXSystemsSupport@essilorusa.com', 'Pcoverru@essilorluxottica.id','QualityDC@essilorusa.com','Customs-ELMTIJ@essilorluxottica.id','juan.vazquez@essilorusa.com','cesar.cortes@essilorusa.com','Erika.Gonzalez@essilorusa.com']

        # Crear el mensaje
        msg = EmailMessage()
        msg['Subject'] = subject
        msg['From'] = 'johan.lozoya@essilorluxottica.id'
        msg['To'] = ', '.join(to_email)  
        msg.set_content(body)

        # Adjuntar Excel si existe
        if excel_file:
            msg.add_attachment(
                excel_file.read(),
                maintype='application',
                subtype='vnd.openxmlformats-officedocument.spreadsheetml.sheet',
                filename=excel_file.filename
            )

        # print("Enviando correo a:", to_email)  # DEBUG

        # Enviar correo
        with smtplib.SMTP('smtp.office365.com', 587) as smtp:
            smtp.starttls()
            smtp.login('johan.lozoya@essilorluxottica.id', 'elpepeBot123!')
            smtp.send_message(msg)

        return jsonify({'message': f'Reporte enviado correctamente a {to_email}.'})
    
    except smtplib.SMTPAuthenticationError:
        return jsonify({'message': 'Error de autenticación SMTP. Verifica las credenciales.'}), 500
    except smtplib.SMTPException as e:
        return jsonify({'message': f'Error SMTP: {str(e)}'}), 500
    except Exception as e:
        return jsonify({'message': f'Error inesperado: {str(e)}'}), 500
