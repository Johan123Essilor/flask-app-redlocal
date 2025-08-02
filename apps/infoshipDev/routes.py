from . import infoship_bp
from flask import render_template

@infoship_bp.route('/direccion')
def direccion():
    return render_template('direccion.html')
