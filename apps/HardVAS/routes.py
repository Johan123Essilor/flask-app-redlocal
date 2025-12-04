from flask import render_template, request, session, jsonify
from apps.auth.utils import login_required
from . import HardVAS_bp


@HardVAS_bp.route('/', methods=['GET'])
@login_required
def index():
    usuario = session.get('usuario')

    return render_template(
        'HardVASIndex.html',

    )