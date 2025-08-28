import requests
import re

API_URL = "http://usmdvulxp019.luxgroup.net:9096/api/wcsdata/GetWhseScans"

def get_by_confirmation(confirmation_nr=None):
    try:
        # ejemplo: 5s para conectar, 60s para respuesta
        response = requests.get(API_URL, timeout=(5, 60))
        response.raise_for_status()
        data = response.json()

        if confirmation_nr:
            confirmation_nr_clean = re.sub(r'\s+', '', confirmation_nr).upper()
            filtered = [
                r for r in data
                if re.sub(r'\s+', '', str(r.get("confirmation_Nr", ""))).upper() == confirmation_nr_clean
            ]
            print(f"Registros encontrados: {len(filtered)}")
            return filtered

        return data
    except requests.exceptions.Timeout:
        print("⏳ La API tardó demasiado en responder (timeout).")
        return []
    except requests.exceptions.RequestException as e:
        print(f"❌ Error al conectar con la API: {e}")
        return []
