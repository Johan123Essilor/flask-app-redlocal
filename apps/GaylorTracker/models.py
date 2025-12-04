import requests
from datetime import datetime
API_URL = "http://10.81.153.123:8000/api/gaylor-tracker/"

def get_all_gaylor(filter_packing=None):
    """
    Obtiene todos los registros desde la API de GaylorTracker
    filtrando por packing_object.
    """
    params = {}
    if filter_packing:
        params['packing_object'] = filter_packing

    try:
        response = requests.get(API_URL, params=params, timeout=10)
        response.raise_for_status()
        return response.json()  # lista de dicts
    except requests.exceptions.RequestException as e:
        print(f"❌ Error al conectar con la API: {e}")
        return []


API_URL_AUDITORY = "http://10.81.153.123:8000/api/gaylor-auditory/"

def save_auditory_record(packing_object, qty, auditor, over, short, dateTime, year, quarter, weekNumber):
    """
    Guarda un registro en la API de GaylorTrackerAudiory
    """
    try:
        print(f"🔍 DEBUG: Intentando guardar en API - PO: {packing_object}")
        
        data = {
            'packing_object': packing_object,
            'qty': qty,
            'auditor': auditor,
            'over': over,
            'short': short,
            'dateTime': dateTime,
            'year': year,
            'quarter': quarter,
            'weekNumber': weekNumber
        }
        
        print(f"🔍 DEBUG: Datos a enviar a API: {data}")
        
        response = requests.post(API_URL_AUDITORY, json=data, timeout=10)
        print(f"🔍 DEBUG: Respuesta API - Status: {response.status_code}, Text: {response.text}")
        
        response.raise_for_status()
        return True
        
    except requests.exceptions.RequestException as e:
        print(f"❌ DEBUG: Error en save_auditory_record: {e}")
        return False
def get_previous_audits(packing_object):
    """
    Obtiene todas las auditorías previas de un packing_object
    """
    try:
        # La API ya tiene filtro por packing_object en la URL
        response = requests.get(f"{API_URL_AUDITORY}?packing_object={packing_object}", timeout=10)
        response.raise_for_status()
        return response.json()  # lista de dicts con auditorías previas
    except requests.exceptions.RequestException as e:
        print(f"❌ Error al obtener auditorías previas: {e}")
        return []    