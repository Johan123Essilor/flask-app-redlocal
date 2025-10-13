import os
from flask import render_template, request, redirect, url_for, flash, session
from werkzeug.utils import secure_filename
from .models import insert_file, get_all_files, delete_file, update_file
from . import VisualAID_bp
from apps.auth.utils import login_required  

UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), 'static', 'uploads')
ALLOWED_EXTENSIONS = {'pdf'}

clientes = sorted([
    'ACADEMY', 'DILLARDS', 'DICKS SPORTING GOODS (DSG)', 'EYEMART EXPRESS', 'REI # DC',
    'THE BUCKLE DC #900 / THE BUCKLE, INC. DC# 900', 'NORDSTROM', 'CHRISTY SPORTS', 'VAIL RESORTS',
    'ALTITUD SPORTS', 'ATALLAH (SSENCE)', 'BACKCOUNTRY', 'BLACK FLAG', 'DESIGNER EYES',
    'DUNHAM SPORTS DC', 'EVO DC', 'FGL SPORTS LTD. GTA DC', 'GLASSES USA',
    'HIBBETT SPORTS / HIBBETT WHOLESALE INC', 'LEGENDS GLOBAL MERCHANDISE', 'MOTOSPORT',
    'MY EYE DOCTOR INC', 'PACSUN', 'PASSION FOR FASHION', 'ROSS', 'The House (HOUSE MINN, HOUSE CALI)',
    'SPORTSMAN & SKI HAUS', 'Carlsgolfland', "Bob's Chalet", 'BIG5 DC',
    'COSTCO WHOLESALE CORP #01100', 'COSTCO OPTICAL LAB #00908', 'COSTCO FREDERICK ECOM #731',
    'COSTCO TRACY ECOM #725', 'COSTCO OPTICAL LAB #00190', 'ESSILOR OF AMERICA', 'SAM’S',
    'SUNSATIONS INTERNATIONAL INC', 'TOWN SQUARE BUSINESS INC', 'Savino Del Bene/ Project Verte',
    'INGRAM MICRO', 'GALLS', 'VGOVX', 'TJ MAXX', 'MARSHALLS', 'Shopko'
], key=lambda x: x.lower())  

codigos = ['US', 'MX']

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@VisualAID_bp.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if not session.get('usuario'):
            flash('Debes iniciar sesión para subir archivos')
            return redirect(url_for('VisualAID.index'))

        file = request.files.get('file')
        cliente = request.form.get('cliente')
        nombre = request.form.get('custom_name')
        codigo = request.form.get('codigo')
        usuario = session.get('usuario')

        if file and allowed_file(file.filename) and cliente and nombre and codigo:
            filename = secure_filename(file.filename)
            os.makedirs(UPLOAD_FOLDER, exist_ok=True)
            file.save(os.path.join(UPLOAD_FOLDER, filename))

            insert_file(filename, nombre, cliente, usuario, codigo)
            flash('Archivo subido correctamente')
            return redirect(url_for('VisualAID.index'))
        else:
            flash('Faltan campos requeridos o el archivo no es válido')
            return redirect(url_for('VisualAID.index'))

    # Obtener filtros
    filter_cliente = request.args.get('filter_cliente')
    filter_author = request.args.get('filter_author')
    filter_name = request.args.get('filter_name')
    filter_codigo = request.args.get('filter_codigo')

    files = get_all_files(
        filter_cliente=filter_cliente,
        filter_author=filter_author,
        filter_name=filter_name,
        filter_codigo=filter_codigo
    )

    return render_template(
        'VisualAIDIndex.html',
        files=files,
        usuario=session.get('usuario'),
        clientes=clientes,
        codigos=codigos,
        filter_cliente=filter_cliente,
        filter_author=filter_author,
        filter_name=filter_name,
        filter_codigo=filter_codigo
    )

@VisualAID_bp.route('/delete/<int:file_id>', methods=['POST'])
@login_required
def delete(file_id):
    filename = delete_file(file_id)
    if filename:
        path = os.path.join(UPLOAD_FOLDER, filename)
        if os.path.exists(path):
            try:
                os.remove(path)
                flash('Archivo eliminado correctamente.')
            except Exception as e:
                flash(f'Error al eliminar el archivo: {e}')
        else:
            flash('El archivo no existe en el sistema de archivos.')
    else:
        flash('Archivo no encontrado en la base de datos.')

    return redirect(url_for('VisualAID.index'))

@VisualAID_bp.route('/update/<int:file_id>', methods=['POST'])
@login_required
def update(file_id):
    new_name = request.form.get('custom_name')
    new_cliente = request.form.get('cliente')
    new_codigo = request.form.get('codigo')
    new_file = request.files.get('file')

    if not new_name or not new_cliente or not new_codigo:
        flash("Todos los campos son obligatorios")
        return redirect(url_for('VisualAID.index'))

    filename = None
    if new_file and allowed_file(new_file.filename):
        filename = secure_filename(new_file.filename)
        os.makedirs(UPLOAD_FOLDER, exist_ok=True)
        new_file.save(os.path.join(UPLOAD_FOLDER, filename))

        # Eliminar archivo anterior si existe
        old = next((f for f in get_all_files() if f['id'] == file_id), None)
        if old:
            old_path = os.path.join(UPLOAD_FOLDER, old['filename'])
            if os.path.exists(old_path):
                try:
                    os.remove(old_path)  # Eliminar archivo anterior
                except Exception as e:
                    flash(f'Error al eliminar el archivo anterior: {e}')
            else:
                flash('El archivo anterior ya no existe en el sistema.')

    # Actualizar la base de datos con los nuevos datos
    update_file(file_id, new_name, new_cliente, new_codigo, filename)

    flash("Archivo actualizado correctamente")
    return redirect(url_for('VisualAID.index'))
