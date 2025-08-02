from flask import Blueprint, render_template

infoship_bp = Blueprint(
    'infoship', __name__,
    template_folder='templates',
    static_folder='static'
)

@infoship_bp.route('/direccion')
def direccion():
    return render_template('direccion.html')
