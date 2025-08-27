import requests

API_URL = "http://usmdvulxp019.luxgroup.net:9096/api/wcsdata/GetWhseScans"

def get_by_confirmation(confirmation_nr=None):
    """
    Obtiene registros desde la API externa y filtra por confirmation_Nr.
    Devuelve TODOS los registros, pero el conteo debe excluir los que
    tienen tote_ID = 'NO-TOTE'.
    """
    try:
        response = requests.get(API_URL, timeout=10)
        response.raise_for_status()
        data = response.json()  # lista de dicts

        if confirmation_nr:
            filtered = [
                r for r in data
                if r.get("confirmation_Nr") == confirmation_nr
            ]
            return filtered

        return []
    except requests.exceptions.RequestException as e:
        print(f"❌ Error al conectar con la API: {e}")
        return []
