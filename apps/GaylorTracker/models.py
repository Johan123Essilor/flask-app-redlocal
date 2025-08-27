import requests

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
