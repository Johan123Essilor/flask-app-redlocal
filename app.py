from flask import Flask, render_template
from jinja2 import ChoiceLoader, FileSystemLoader

app = Flask(__name__)

app.jinja_loader = ChoiceLoader([
    app.jinja_loader,
    FileSystemLoader('apps/cubo/templates'),
    FileSystemLoader('apps/infoshipDev/templates')
])

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
    app.run(debug=True)


