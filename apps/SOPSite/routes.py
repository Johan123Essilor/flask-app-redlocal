import os
from flask import render_template, request, redirect, url_for, flash, session
from werkzeug.utils import secure_filename
from .models import insert_file, get_all_files, delete_file
from . import SOPSite_bp
from apps.auth.utils import login_required  

UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), 'static', 'uploads')
ALLOWED_EXTENSIONS = {'pdf'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Puedes definir las áreas permitidas si deseas mostrarlas dinámicamente
AREAS = ['Training', 'Continuous Improvement', 'Engagement', 'Engineering', 'Customer Service', 'Allocation', 'Customer Service', 'Simulation & Capacity', 'Slotting'
         , 'Quality', 'Inventory', 'Business Intelligence', 'Business Systems', 'Transportation', 'Operations']

@SOPSite_bp.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if not session.get('usuario'):
            flash('Debes iniciar sesión para subir archivos')
            return redirect(url_for('SOPSite.index'))

        file = request.files.get('file')
        area = request.form.get('area')
        nombre = request.form.get('custom_name')  # Campo nombre desde el formulario
        usuario = session.get('usuario')  # Creador desde sesión

        if file and allowed_file(file.filename) and area and nombre:
            filename = secure_filename(file.filename)
            os.makedirs(UPLOAD_FOLDER, exist_ok=True)
            file.save(os.path.join(UPLOAD_FOLDER, filename))

            insert_file(filename, nombre, area, usuario)
            flash('Archivo subido correctamente')
            return redirect(url_for('SOPSite.index'))
        else:
            flash('Faltan campos requeridos o el archivo no es válido')
            return redirect(url_for('SOPSite.index'))

    # GET: obtén filtros de la query string
    filter_area = request.args.get('filter_area')
    filter_author = request.args.get('filter_author')
    filter_name = request.args.get('filter_name')


    files = get_all_files(filter_area=filter_area, filter_author=filter_author, filter_name=filter_name)

    return render_template(
        'SOPSiteIndex.html',
        files=files,
        usuario=session.get('usuario'),
        areas=AREAS,
        filter_area=filter_area,
        filter_author=filter_author,
        filter_name=filter_name  # ← aquí también
    )


@SOPSite_bp.route('/delete/<int:file_id>')
@login_required
def delete(file_id):
    filename = delete_file(file_id)
    if filename:
        path = os.path.join(UPLOAD_FOLDER, filename)
        if os.path.exists(path):
            os.remove(path)
        flash('Archivo eliminado')
    else:
        flash('Archivo no encontrado')
    return redirect(url_for('SOPSite.index'))
