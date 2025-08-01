# Flask App - Red Local

Esta es una aplicación web desarrollada en Flask que corre en una red local o en una Raspberry Pi como servidor.

## 🚀 Cómo iniciar

### 1. Clona el repositorio

```bash
git clone https://github.com/Johan123Essilor/flask-app-redlocal.git
cd flask-app-redlocal

python -m venv venv
# En Windows
venv\Scripts\activate
# En Linux/Mac
source venv/bin/activate


pip install -r requirements.txt


python app.py


flask-app-redlocal/
├── app.py
├── requirements.txt
├── README.md
├── .gitignore
├── templates/
│   └── index.html
└── apps/
    ├── cubo/
    │   └── templates/
    │       └── cubo.html
    └── infoshipDev/
        └── templates/
            └── index.html
