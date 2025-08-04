from flask import Flask, render_template, abort
from apps.infoshipDev import infoship_bp
from apps.SOPSite import SOPSite_bp
from apps.auth.routes import auth_bp
from datetime import timedelta
from jinja2 import ChoiceLoader, FileSystemLoader
import json

app = Flask(__name__)
app.secret_key = 'una_clave_super_secreta'
app.permanent_session_lifetime = timedelta(minutes=30)
app.jinja_loader = ChoiceLoader([
    app.jinja_loader,
    FileSystemLoader('apps/cubo/templates'),
    FileSystemLoader('apps/infoshipDev/templates'),
    FileSystemLoader('apps/SOPSite/templates')
])


def cargar_datos():
    with open('static/data/clients.json', 'r', encoding='utf-8') as f:
        return json.load(f)


@app.route('/')
def home():
    return render_template('index.html')  # Puede quedar como plantilla global
@app.route('/landing')
def landing():
    return render_template('landingPague.html')  # Puede quedar como plantilla global
#---------------------------------3D View
@app.route('/cubo')
def cubo():
    return render_template('cubo.html')
@app.route('/visor/<int:item_id>')
def visor(item_id):
    clientes = cargar_datos()
    if item_id < 0 or item_id >= len(clientes):
        abort(404)
    cliente = clientes[item_id]
    return render_template('visor.html', cliente=cliente)

#---------------------------------Infoship
app.register_blueprint(infoship_bp, url_prefix='/infoship')
@app.route('/infoship')
def infoship():
    return render_template('infoshipDevIndex.html')
@app.route('/infoship/direccion')
def direccion():
    return render_template('direccion.html')
@app.route('/infoship/carrierChange')
def carrierChange():
    return render_template('Cambio de carrier.html')



#---------------------------------SOPSite
app.register_blueprint(SOPSite_bp, url_prefix='/SOPSite')

#---------------------------------Auth
app.register_blueprint(auth_bp, url_prefix='/auth')




if __name__ == '__main__':
    app.run(host="0.0.0.0", port=9818,debug=False)

    # app.run(debug=True)


