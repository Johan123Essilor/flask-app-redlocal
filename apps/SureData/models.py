import requests
import re

API_URL = "http://usmdvulxp019.luxgroup.net:9096/api/wcsdata/GetWhseScans"

def get_by_confirmation(confirmation_nr=None):
    try:
        response = requests.get(API_URL, timeout=10)
        response.raise_for_status()
        data = response.json()

        if confirmation_nr:
            # Limpieza robusta: mayúsculas y eliminar espacios o caracteres invisibles
            confirmation_nr_clean = re.sub(r'\s+','',confirmation_nr).upper()
            filtered = [
                r for r in data
                if re.sub(r'\s+','',str(r.get("confirmation_Nr",""))).upper() == confirmation_nr_clean
            ]
            print(f"Registros encontrados: {len(filtered)}")
            return filtered

        return data  # devuelve todos si no hay filtro
    except requests.exceptions.RequestException as e:
        print(f"❌ Error al conectar con la API: {e}")
        return []
