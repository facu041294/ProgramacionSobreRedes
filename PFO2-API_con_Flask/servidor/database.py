# Módulo para toda la interacción con SQLite
# servidor/database.py

import sqlite3

DB_NAME = "tareas.db"

def inicializar_db():
    """
    Crea la base de datos y la tabla de usuarios si no existen.
    Esta función se llamará una sola vez, al iniciar el servidor.
    """
    # 'with' asegura que la conexión se cierre incluso si hay errores.
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        # Creamos la tabla 'usuarios' con un campo 'usuario' único para evitar duplicados.
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS usuarios (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                usuario TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL
            )
        """)
        conn.commit()
        print("Base de datos inicializada correctamente.")

def crear_usuario(usuario, password_hash):
    """
    Inserta un nuevo usuario en la base de datos.
    Devuelve True si fue exitoso, False si el usuario ya existe.
    """
    try:
        with sqlite3.connect(DB_NAME) as conn:
            cursor = conn.cursor()
            # Usamos parámetros (?) para prevenir inyección SQL.
            cursor.execute("INSERT INTO usuarios (usuario, password_hash) VALUES (?, ?)", (usuario, password_hash))
            conn.commit()
        return True
    except sqlite3.IntegrityError:
        # Esto ocurre si intentamos insertar un 'usuario' que ya existe (por la restricción UNIQUE).
        return False

def obtener_usuario(usuario):
    """
    Busca un usuario por su nombre de usuario.
    Devuelve los datos del usuario como un diccionario si lo encuentra, o None si no.
    """
    with sqlite3.connect(DB_NAME) as conn:
        # Le decimos a la conexión que devuelva las filas como diccionarios.
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM usuarios WHERE usuario = ?", (usuario,))
        user_row = cursor.fetchone() # fetchone() obtiene la primera (y única) fila.
        
        # Convertimos la fila a un diccionario estándar para que sea más fácil de usar.
        if user_row:
            return dict(user_row)
        return None