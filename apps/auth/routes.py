from flask import Blueprint, render_template, request, session, redirect, url_for, flash
from apps.auth.models import validate_login
auth_bp = Blueprint('auth', __name__, template_folder='templates')





@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['usuario']
        password = request.form['password']
        if validate_login(username, password):
            session['usuario'] = username
            flash('Sesión iniciada con éxito')
            return redirect(url_for('SOPSite.index'))  # Cambia según tu blueprint
        else:
            flash('Credenciales inválidas')
    return render_template('login.html')


@auth_bp.route('/logout')
def logout():
    session.pop('usuario', None)
    flash('Sesión cerrada')
    return redirect(url_for('home'))
