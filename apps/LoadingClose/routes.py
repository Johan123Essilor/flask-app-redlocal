import os
from flask import render_template, request, redirect, url_for, flash, session
from .models import insert_shipping, get_all_shipping, delete_shipping
from . import ShippingClose_bp
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
        comentarios = request.form.get('comentarios')

        # Validación simple
        if not (anden and tipo_envio and qty and completo and dest):
            flash('Por favor completa todos los campos requeridos')
            return redirect(url_for('ShippingClose.index'))

        # Convierte qty y sellos a enteros
        try:
            qty = int(qty)
        except ValueError:
            flash('Cantidad de pallets y sellos deben ser números válidos')
            return redirect(url_for('ShippingClose.index'))

        # Inserta en la base de datos, pasando el usuario
        insert_shipping(
            andenNo=anden,
            tipo=tipo_envio,
            qty=qty,
            sellos=sellos,
            completo=completo,
            destino=dest,
            comentarios=comentarios,
            usuario=usuario  # PASAMOS el usuario aquí
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
