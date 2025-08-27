from apps.auth.models import init_users, add_user
from datetime import datetime

# Crear usuario con área
username = 'Israel Lopez Padilla'
password = 'ELMPass2025'
area = 'training'

# Llamada a la función original
add_user(username, password, area)

# Guardar en archivo de registro
with open("usuarios.txt", "a", encoding="utf-8") as f:
    f.write(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} | Usuario: {username} | Área: {area}\n")

print("Usuario creado y registrado en usuarios.txt.")
