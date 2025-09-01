# Lógica de la base de datos (SQLite)

# db_manager.py
import sqlite3
import threading

# Un Lock global para proteger la escritura en la base de datos desde múltiples hilos.
# Es CRUCIAL para la versión multi-threaded.
db_lock = threading.Lock()

def setup_database(db_name="chat.db"):
    """Crea la tabla de mensajes si no existe."""
    with sqlite3.connect(db_name) as conn:
        cursor = conn.cursor()
        # Usamos 'IF NOT EXISTS' para que el script se pueda ejecutar múltiples veces sin error.
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS mensajes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                contenido TEXT NOT NULL,
                fecha_envio TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                ip_cliente TEXT NOT NULL
            )
        """)
        conn.commit()

def guardar_mensaje(contenido, ip_cliente, db_name="chat.db"):
    """
    Guarda un mensaje en la base de datos de forma segura para hilos (thread-safe).
    """
    # Adquirimos el lock antes de realizar cualquier operación de escritura.
    with db_lock:
        try:
            # Usamos 'with' para la conexión para asegurar que se cierre correctamente.
            with sqlite3.connect(db_name) as conn:
                cursor = conn.cursor()
                # Usamos parámetros (?) para prevenir inyección SQL.
                cursor.execute(
                    "INSERT INTO mensajes (contenido, ip_cliente) VALUES (?, ?)",
                    (contenido, ip_cliente)
                )
                conn.commit()
            return True # Retorna True si la inserción fue exitosa.
        except sqlite3.Error as e:
            # Capturamos cualquier error de la base de datos.
            print(f"Error en la base de datos: {e}")
            return False # Retorna False si hubo un error.