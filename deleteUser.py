# archivo: borrar_y_crear.py

from apps.auth.models import delete_user, add_user
from datetime import datetime

# 1️⃣ Borrar usuario con ID 10
delete_user(10)

# # 2️⃣ Crear un nuevo usuario
# username = 'Customer Service'
# password = 'ELMPass2025'
# area = 'customer_service'

# add_user(username, password, area)

# # 3️⃣ Guardar registro
# with open("usuarios.txt", "a", encoding="utf-8") as f:
#     f.write(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} | Usuario: {username} | Área: {area}\n")

# print("Usuario creado y registrado en usuarios.txt.")
