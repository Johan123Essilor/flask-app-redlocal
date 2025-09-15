import sqlite3
import re
from datetime import datetime, timedelta
from urllib.parse import urlencode
import requests
import os
from concurrent.futures import ThreadPoolExecutor, TimeoutError
# 🔹 Ruta absoluta para la DB
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DB_PATH = os.path.join(BASE_DIR, 'confirmation_tracker.db')

# -----------------------------
# 🔹 Inicialización de la DB
# -----------------------------
def init_db():
    """Crea la base de datos y tabla si no existen"""
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS confirmation_summaries (
                confirmation_nr TEXT PRIMARY KEY,
                bin_Id TEXT,
                total_hus INTEGER DEFAULT 0,
                encontrados INTEGER DEFAULT 0,
                overs INTEGER DEFAULT 0,
                shorts INTEGER DEFAULT 0,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
        ''')

        conn.commit()


# Llamamos init_db automáticamente al importar models
init_db()

# -----------------------------
# 🔹 Función para insertar resumen
# -----------------------------
def insert_summary(confirmation_nr, bin_Id=None, total_hus=0, encontrados=0, overs=0, shorts=0):
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO confirmation_summaries 
            (confirmation_nr, bin_Id, total_hus, encontrados, overs, shorts, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(confirmation_nr) DO UPDATE SET
                bin_Id=excluded.bin_Id,
                total_hus=excluded.total_hus,
                encontrados=excluded.encontrados,
                overs=excluded.overs,
                shorts=excluded.shorts,
                created_at=excluded.created_at
        ''', (
            confirmation_nr,
            bin_Id,
            total_hus,
            encontrados,
            overs,
            shorts,
            datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
        ))
        conn.commit()
        return confirmation_nr


# -----------------------------
# 🔹 Funciones de consulta API
# -----------------------------
API_URL = "http://usmdvulxp019.luxgroup.net:9096/api/wcsdata/GetWhseScans"

def get_by_confirmation(confirmation_nr, horas_atras=10, max_total_time=20):
    """
    Consulta la API y filtra por confirmation_nr.
    ⏳ Nunca tarda más de `max_total_time` segundos en total.
    """
    try:
        ahora = datetime.utcnow()
        fecha_desde = ahora - timedelta(hours=horas_atras)

        params = {
            'insert_TS_from': fecha_desde.strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z',
            'insert_TS_to': ahora.strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z'
        }

        url = f"{API_URL}?{urlencode(params)}"
        print(f"⚡ Consultando API (rango reducido: {horas_atras}h)...")

        def do_request():
            resp = requests.get(url, timeout=(5, 20))  # 3s conectar, 10s entre bytes
            resp.raise_for_status()
            return resp.json()

        # Ejecutamos en un hilo con límite total
        with ThreadPoolExecutor(max_workers=1) as executor:
            future = executor.submit(do_request)
            try:
                data = future.result(timeout=max_total_time)  # ⏳ límite total
            except TimeoutError:
                print(f"⏳ Timeout total - La API tardó más de {max_total_time}s, abortando.")
                return []

        # Filtrado de resultados
        confirmation_nr_clean = re.sub(r'\s+', '', confirmation_nr).upper()
        filtered = [
            r for r in data
            if re.sub(r'\s+', '', str(r.get("confirmation_Nr", ""))).upper() == confirmation_nr_clean
        ]

        print(f"✅ {len(filtered)} registros encontrados en {len(data)} totales")
        return filtered

    except requests.exceptions.Timeout:
        print("⏳ Timeout - La API no respondió dentro de los límites parciales")
        return []
    except requests.exceptions.RequestException as e:
        print(f"❌ Error de conexión: {e}")
        return []
    except Exception as e:
        print(f"⚠️ Error inesperado: {e}")
        return []

def get_multiple_fields(filters_dict, horas_atras=3):
    try:
        ahora = datetime.utcnow()
        fecha_desde = ahora - timedelta(hours=horas_atras)

        params = {
            'insert_TS_from': fecha_desde.strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z',
            'insert_TS_to': ahora.strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z'
        }

        url = f"{API_URL}?{urlencode(params)}"
        print(f"⚡ Consultando API con {len(filters_dict)} filtros...")

        response = requests.get(url, timeout=(3, 30))
        response.raise_for_status()
        data = response.json()

        filtered = data
        for field, value in filters_dict.items():
            value_clean = re.sub(r'\s+', '', str(value)).upper()
            filtered = [
                r for r in filtered
                if re.sub(r'\s+', '', str(r.get(field, ""))).upper() == value_clean
            ]

        print(f"✅ {len(filtered)} registros encontrados")
        return filtered

    except Exception as e:
        print(f"❌ Error: {e}")
        return []
