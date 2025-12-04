import requests

API_URL = "http://10.81.153.123:8000/api/api_inbound/"

def get_all_HU(filter_HU=None):
    """
    Obtiene todos los registros desde la API de api_inbound
    filtrando por HU.
    """
    params = {}
    if filter_HU:
        params['hu_number'] = filter_HU  # ✅ nombre correcto del parámetro

    try:
        response = requests.get(API_URL, params=params, timeout=10)
        response.raise_for_status()
        return response.json()  # lista de dicts
    except requests.exceptions.RequestException as e:
        print(f"❌ Error al conectar con la API: {e}")
        return []
