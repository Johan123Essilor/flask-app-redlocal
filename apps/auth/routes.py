from flask import Blueprint, render_template, request, session, redirect, url_for, flash
from apps.auth.models import validate_login, update_password, get_user_area

auth_bp = Blueprint('auth', __name__, template_folder='templates')


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Normalizamos el username para evitar espacios al inicio/final
        username = request.form['usuario'].strip()
        password = request.form['password']

        login_correcto, es_primer_login = validate_login(username, password)

        # print(f"Intento de login: username='{username}', login_correcto={login_correcto}")

        if login_correcto:
            # Guardamos usuario en sesión
            session['usuario'] = username

            # Obtenemos el área del usuario
            area = get_user_area(username)
            # print(f"Área obtenida de la DB: '{area}'")

            # Normalizamos el área y la guardamos en sesión
            session['area'] = area.strip().lower() if area else ''
            # print(f"Área guardada en session['area']: '{session['area']}'")

            flash('Sesión iniciada con éxito')

            if es_primer_login:
                flash('Es tu primer inicio de sesión, por favor cambia tu contraseña.')
                return redirect(url_for('auth.change_password'))

            return redirect(url_for('home'))  # Ajusta según tu blueprint
        else:
            flash('Credenciales inválidas')
            # print(f"Login fallido para usuario '{username}'")
            
    return render_template('login.html')


@auth_bp.route('/logout')
def logout():
    session.pop('usuario', None)
    session.pop('area', None)  # También eliminamos el área al cerrar sesión
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
