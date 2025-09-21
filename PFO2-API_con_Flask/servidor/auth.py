# Módulo para la lógica de hashing y verificación de contraseñas
# servidor/auth.py

# Werkzeug es una librería de herramientas WSGI muy potente. 
# Flask está construido sobre ella. Usaremos su módulo de seguridad para el hashing.
# Necesitarás instalarla: pip install Werkzeug
from werkzeug.security import generate_password_hash, check_password_hash

def hashear_password(password_en_texto_plano):
    """
    Toma una contraseña en texto plano y devuelve su representación 'hasheada'.
    El 'hash' incluye el algoritmo usado y un 'salt' aleatorio, 
    por lo que dos hashes de la misma contraseña nunca serán idénticos.
    """
    # 'pbkdf2:sha256' es un algoritmo de hashing moderno y seguro.
    # El '8' es el número de caracteres del 'salt'.
    return generate_password_hash(password_en_texto_plano, method='pbkdf2:sha256:8')

def verificar_password(password_hasheada, password_en_texto_plano):
    """
    Compara una contraseña en texto plano con un hash guardado.
    Devuelve True si coinciden, False en caso contrario.
    Werkzeug se encarga de extraer el salt y el método del hash para la comparación.
    """
    return check_password_hash(password_hasheada, password_en_texto_plano)