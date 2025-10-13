import os
from flask import render_template, request, redirect, url_for, flash, session
from .models import insert_shipping, get_all_shipping, delete_shipping
from . import ShippingClose_bp
from .models import get_all_shipping, toggle_vuelta_en_u_db
from apps.auth.utils import login_required  


TIPOS_ENVIO = ['Frames', 'Frames Mix', 'Merge', 'Ecommerce', 'UPS MX', 'DHL MX', 'WEB PREM', 'Sams RX', 'Locales', 'Oakley']

@ShippingClose_bp.route('/', methods=['GET', 'POST'])
def index():
    usuario = session.get('usuario')

    if request.method == 'POST':
        if not usuario:
            flash('Debes iniciar sesión para registrar datos')
            return redirect(url_for('ShippingClose.index'))

        # Obtén los datos del formulario
        anden = request.form.get('anden')
        tipo_envio = request.form.get('type')
        qty = request.form.get('qty')
        sellos = request.form.get('sellos') or 0
        completo = request.form.get('completo')
        dest = request.form.get('dest')
        caja_pacas = request.form.get('caja_pacas') 
        comentarios = request.form.get('comentarios')
        gaylord = request.form.get('gaylord')
        truck_id = request.form.get('truck_id')
        vuelta_en_u = request.form.get('vuelta_en_u') == "true"

        # Validación simple
        if not (anden and tipo_envio and qty and completo and dest and gaylord and truck_id):
            flash('Por favor completa todos los campos requeridos')
            return redirect(url_for('ShippingClose.index'))

        # Convierte qty a entero
        try:
            qty = int(qty)
        except ValueError:
            flash('Cantidad de pallets debe ser un número válido')
            return redirect(url_for('ShippingClose.index'))

        # Inserta en la base de datos
        insert_shipping(
            andenNo=anden,
            tipo=tipo_envio,
            qty=qty,
            sellos=sellos,
            completo=completo,
            destino=dest,
            comentarios=comentarios,
            caja_pacas=caja_pacas,
            gaylord=gaylord,
            truck_id=truck_id,
            vuelta_en_u=vuelta_en_u,
            usuario=usuario
        )
        flash('Registro guardado correctamente')
        return redirect(url_for('ShippingClose.index'))

    # GET: filtros para mostrar la tabla
    filter_type = request.args.get('filter_type')

    registros = get_all_shipping(filter_type=filter_type)

    return render_template(
        'ShippingCloseIndex.html',
        registros=registros,
        usuario=usuario,
        tipos_envio=TIPOS_ENVIO,
        filter_type=filter_type
    )

@ShippingClose_bp.route('/delete/<int:registro_id>')
@login_required
def delete(registro_id):
    success = delete_shipping(registro_id)
    if success:
        flash('Registro eliminado')
    else:
        flash('Registro no encontrado')
    return redirect(url_for('ShippingClose.index'))


from .models import get_all_shipping, toggle_vuelta_en_u_db

@ShippingClose_bp.route("/toggle_vuelta_en_u/<int:registro_id>", methods=["POST"])
@login_required
def toggle_vuelta_en_u(registro_id):
    usuario_area = session.get("area")
    if usuario_area != "customer_service":
        flash("No tienes permisos para cambiar este valor.", "danger")
        return redirect(url_for("ShippingClose.index"))

    registros = get_all_shipping()
    registro_actual = next((r for r in registros if r['id'] == registro_id), None)

    if not registro_actual:
        flash("Registro no encontrado", "danger")
        return redirect(url_for("ShippingClose.index"))

    nuevo_valor = not registro_actual['vuelta_en_u']
    toggle_vuelta_en_u_db(registro_id, nuevo_valor)

    flash("Valor de 'Vuelta en U' actualizado correctamente.", "success")
    return redirect(url_for("ShippingClose.index"))
