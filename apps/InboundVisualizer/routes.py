from flask import render_template, request, session, jsonify
from apps.auth.utils import login_required
from .models import get_all_HU
import smtplib
from flask import request, jsonify
import requests

from email.message import EmailMessage
from email.message import EmailMessage
from datetime import datetime
import json, smtplib
from office365.runtime.auth.user_credential import UserCredential
from office365.sharepoint.client_context import ClientContext
import os
from . import inboundVisualizer_bp  # Importar el Blueprint desde __init__.py

# Ruta principal para mostrar el tracker
@inboundVisualizer_bp.route('/', methods=['GET'])
@login_required  # Descomentar si se quiere proteger
def index():
    usuario = session.get('usuario')
    filter_HU = request.args.get('hu_number')  

    registros = []
    total_resultados = 0
    handling_units_count = 0

    if filter_HU:
        registros = get_all_HU(filter_HU=filter_HU)
        total_resultados = len(registros)
        handling_units_count = len(registros) if registros else 0


    return render_template(
        'InboundVisualizerIndex.html',
        registros=registros,
        usuario=usuario,
        filter_HU=filter_HU,
        total_resultados=total_resultados,
        handling_units_count=handling_units_count
    )

@inboundVisualizer_bp.route('/update_completo', methods=['POST'])
@login_required
def update_completo():
    data = request.json
    record_id = data.get('id')
    completo = data.get('completo')

    if record_id is None or completo is None:
        return jsonify({'success': False, 'message': 'Faltan parámetros'}), 400

    try:
        print(f"Actualizando record {record_id} a completo={completo}")
        response = requests.patch(
            f"http://10.81.153.123:8000/api/api_inbound/{record_id}/",
            json={"completo": completo},
            timeout=10
        )
        print("Respuesta API:", response.text)
        response.raise_for_status()
        return jsonify({'success': True, 'message': f'Registro {record_id} actualizado correctamente'})

    except requests.exceptions.RequestException as e:
        print('Error al conectar con la API:', e)
        return jsonify({'success': False, 'message': str(e)}), 500


# @gaylorTracker_bp.route('/send_report', methods=['POST'])
# @login_required
# def send_report():
#     usuario = session.get('usuario', 'Desconocido')

#     try:
#         subject = request.form.get('subject', 'Reporte sin asunto')
#         body = request.form.get('body', '')
#         excel_file = request.files.get('excel_file')
#         packing_object = request.form.get('packing_object', 'Sin Packing Object')

#         # Agregar auditor al cuerpo del mensaje
#         body += f"\n\nAuditor: {usuario}"

#         # Destinatario fijo
#         to_email = [
#             'MXSystemsSupport@essilorusa.com', 
#             'Pcoverru@essilorluxottica.id',
#             'QualityDC@essilorusa.com',
#             'Customs-ELMTIJ@essilorluxottica.id',
#             'juan.vazquez@essilorusa.com',
#             'cesar.cortes@essilorluxottica.com',
#             'Erika.Gonzalez@essilorluxottica.com'
#         ]

#         # Crear el mensaje
#         msg = EmailMessage()
#         msg['Subject'] = subject
#         msg['From'] = 'johan.lozoya@essilorluxottica.id'
#         msg['To'] = ', '.join(to_email)  
#         msg.set_content(body)

#         # Adjuntar Excel si existe
#         if excel_file:
#             msg.add_attachment(
#                 excel_file.read(),
#                 maintype='application',
#                 subtype='vnd.openxmlformats-officedocument.spreadsheetml.sheet',
#                 filename=excel_file.filename
#             )

#         # Enviar correo
#         with smtplib.SMTP('smtp.office365.com', 587) as smtp:
#             smtp.starttls()
#             smtp.login('johan.lozoya@essilorluxottica.id', 'elpepeBot123!')
#             smtp.send_message(msg)

#         # ====== Guardar solo Packing Object en SharePoint ======
#         from office365.runtime.auth.user_credential import UserCredential
#         from office365.sharepoint.client_context import ClientContext

#         site_url = "https://luxotticagroup.sharepoint.com/sites/AtlantaDCSupportCenter"
#         list_name = "Tijuana DC Requests"

#         ctx = ClientContext(site_url).with_credentials(
#             UserCredential("johan.lozoya@essilorluxottica.id", "elpepeBot123!")
#         )

#         sp_list = ctx.web.lists.get_by_title(list_name)
#         sp_list.add_item({"Title": packing_object}).execute_query()

#         return jsonify({'message': f'Reporte enviado correctamente a {to_email} y registrado en SharePoint con Packing Object: {packing_object}.'})

#     except Exception as e:
#         return jsonify({'message': f'Error inesperado: {str(e)}'}), 500
    











# @gaylorTracker_bp.route('/send_report', methods=['POST'])
# @login_required
# def send_report():
#     usuario = session.get('usuario', 'Desconocido')

#     try:
#         subject = request.form.get('subject', 'Reporte sin asunto')
#         body = request.form.get('body', '')
#         excel_file = request.files.get('excel_file')

#         # Agregar auditor al cuerpo del mensaje
#         body += f"\n\nAuditor: {usuario}"

#         # Destinatario fijo
#         to_email = ['MXSystemsSupport@essilorusa.com', 'Pcoverru@essilorluxottica.id','QualityDC@essilorusa.com','Customs-ELMTIJ@essilorluxottica.id','juan.vazquez@essilorusa.com','cesar.cortes@essilorusa.com','Erika.Gonzalez@essilorusa.com']

#         # Crear el mensaje
#         msg = EmailMessage()
#         msg['Subject'] = subject
#         msg['From'] = 'johan.lozoya@essilorluxottica.id'
#         msg['To'] = ', '.join(to_email)  
#         msg.set_content(body)

#         # Adjuntar Excel si existe
#         if excel_file:
#             msg.add_attachment(
#                 excel_file.read(),
#                 maintype='application',
#                 subtype='vnd.openxmlformats-officedocument.spreadsheetml.sheet',
#                 filename=excel_file.filename
#             )

#         # print("Enviando correo a:", to_email)  # DEBUG

#         # Enviar correo
#         with smtplib.SMTP('smtp.office365.com', 587) as smtp:
#             smtp.starttls()
#             smtp.login('johan.lozoya@essilorluxottica.id', 'elpepeBot123!')
#             smtp.send_message(msg)

#         return jsonify({'message': f'Reporte enviado correctamente a {to_email}.'})
    
#     except smtplib.SMTPAuthenticationError:
#         return jsonify({'message': 'Error de autenticación SMTP. Verifica las credenciales.'}), 500
#     except smtplib.SMTPException as e:
#         return jsonify({'message': f'Error SMTP: {str(e)}'}), 500
#     except Exception as e:
#         return jsonify({'message': f'Error inesperado: {str(e)}'}), 500


# @gaylorTracker_bp.route('/send_report', methods=['POST'])
# @login_required
# def send_report():


#     try:
#         usuario = session.get('usuario', 'Desconocido')
#         subject = request.form.get('subject', 'Reporte sin asunto')
#         body = request.form.get('body', '')
#         excel_file = request.files.get('excel_file')
#         over_hus = json.loads(request.form.get('over_hus', '[]'))
#         short_hus = json.loads(request.form.get('short_hus', '[]'))
#         hu_fisicos = request.form.get('huFisicos', '0')
#         hu_sap = request.form.get('huRegistrados', '0')
#         linea = request.form.get('linea', 'Desconocido')
#         carrier = request.form.get('carrier', 'Desconocido')

#         # Determinar tipo de hallazgo
#         if over_hus and short_hus:
#             tipo_hallazgo = "Over y Short"
#         elif over_hus:
#             tipo_hallazgo = "Over"
#         elif short_hus:
#             tipo_hallazgo = "Short"
#         else:
#             tipo_hallazgo = "Sin hallazgos"

#         # Cuerpo final
#         body_final = body
#         body_final += f"\n\nAuditor: {usuario}\nLinea: {linea}\nCarrier: {carrier}"

#         # Crear asunto con fecha
#         fechaHora = datetime.now().strftime("%d/%m/%Y, %H:%M:%S")
#         subject_final = f"{subject}"

#         # Destinatarios de producción
#         to_email = [
#             # 'MXSystemsSupport@essilorusa.com',
#             'Pcoverru@essilorluxottica.id',
#             'QualityDC@essilorusa.com',
#             'Customs-ELMTIJ@essilorluxottica.id',
#             'juan.vazquez@essilorusa.com',
#             'cesar.cortes@essilorluxottica.com',
#             'Erika.Gonzalez@essilorluxottica.com'
#             # 'johan.lozoya@essilorluxottica.id'
#         ]

#         # Crear correo
#         msg = EmailMessage()
#         msg['Subject'] = subject_final
#         msg['From'] = 'johan.lozoya@essilorluxottica.id'
#         msg['To'] = ', '.join(to_email)
#         msg.set_content(body_final)

#         # Adjuntar Excel
#         if excel_file:
#             msg.add_attachment(
#                 excel_file.read(),
#                 maintype='application',
#                 subtype='vnd.openxmlformats-officedocument.spreadsheetml.sheet',
#                 filename=excel_file.filename
#             )

#         # Enviar correo
#         with smtplib.SMTP('smtp.office365.com', 587) as smtp:
#             smtp.starttls()
#             smtp.login('johan.lozoya@essilorluxottica.id', 'elpepeBot123!')
#             smtp.send_message(msg)

#         return jsonify({'message': f'Reporte enviado correctamente ({tipo_hallazgo}).'})

#     except Exception as e:
#         return jsonify({'message': f'Error inesperado: {str(e)}'}), 500
