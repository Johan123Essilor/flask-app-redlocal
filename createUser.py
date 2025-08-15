from apps.auth.models import init_users, add_user

# Crear usuario con área
add_user('admin', 'ELMPass2025', 'admin')  # 'admin' es el área

print("Usuario creado.")
