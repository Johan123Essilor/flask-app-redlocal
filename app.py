from flask import Flask, render_template, abort
from jinja2 import ChoiceLoader, FileSystemLoader
import json

app = Flask(__name__)

app.jinja_loader = ChoiceLoader([
    app.jinja_loader,
    FileSystemLoader('apps/cubo/templates'),
    FileSystemLoader('apps/infoshipDev/templates')
])


def cargar_datos():
    with open('static/data/clients.json', 'r', encoding='utf-8') as f:
        return json.load(f)

@app.route('/visor/<int:item_id>')
def visor(item_id):
    clientes = cargar_datos()
    if item_id < 0 or item_id >= len(clientes):
        abort(404)
    cliente = clientes[item_id]
    return render_template('visor.html', cliente=cliente)

@app.route('/')
def home():
    return render_template('index.html')  # Puede quedar como plantilla global

@app.route('/cubo')
def cubo():
    return render_template('cubo.html')

@app.route('/infoship')
def infoship():
    return render_template('infoship/index.html')


if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)

    # app.run(debug=True)


