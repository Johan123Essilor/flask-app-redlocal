from flask import Blueprint, render_template, request, session, redirect, url_for, flash
from apps.auth.models import validate_login, update_password

auth_bp = Blueprint('auth', __name__, template_folder='templates')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['usuario']
        password = request.form['password']
        
        login_correcto, es_primer_login = validate_login(username, password)

        if login_correcto:
            session['usuario'] = username
            flash('Sesión iniciada con éxito')

            if es_primer_login:
                flash('Es tu primer inicio de sesión, por favor cambia tu contraseña.')
                return redirect(url_for('auth.change_password'))
            
            return redirect(url_for('home'))  # Cambia según tu blueprint
        else:
            flash('Credenciales inválidas')
    return render_template('login.html')


@auth_bp.route('/logout')
def logout():
    session.pop('usuario', None)
    flash('Sesión cerrada')
    return redirect(url_for('home'))


@auth_bp.route('/change_password', methods=['GET', 'POST'])
def change_password():
    if 'usuario' not in session:
        flash('Por favor, inicia sesión primero.')
        return redirect(url_for('auth.login'))

    if request.method == 'POST':
        nueva_contraseña = request.form['nueva_password']
        confirmar = request.form['confirmar_password']

        if nueva_contraseña != confirmar:
            flash('Las contraseñas no coinciden')
            return redirect(url_for('auth.change_password'))

        update_password(session['usuario'], nueva_contraseña)
        flash('Contraseña cambiada con éxito')
        return redirect(url_for('home'))  # Después de cambiar, va al inicio

    return render_template('change_password.html')
