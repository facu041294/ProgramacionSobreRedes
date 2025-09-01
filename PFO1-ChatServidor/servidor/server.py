# Script principal del servidor

# server.py
import socket
import threading
from . import db_manager
from .client_handler import handle_client # Importamos la función del otro archivo

HOST = '127.0.0.1'  # localhost
PORT = 5000

# Creamos un Event para controlar el bucle principal del servidor.
shutdown_event = threading.Event()

def init_socket(host, port):
    """Inicializa y retorna el socket del servidor."""
    try:
        # Crear un socket TCP/IP (AF_INET = IPv4, SOCK_STREAM = TCP)
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        # Linea 23 permite reutilizar la dirección del socket inmediatamente, útil para reinicios rápidos
        # NOTA: En algunos SOs, esto puede permitir que múltiples servidores se bindeen al mismo puerto. (Me pasó en Windows 10)
        # server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        # Vincular el socket al host y puerto especificados.
        server_socket.bind((host, port))
        
        # Poner el socket en modo de escucha, aceptando hasta 5 conexiones en cola.
        server_socket.listen(5)
        print(f"[*] Servidor escuchando en {host}:{port}")
        return server_socket
    except OSError as e:
        # Manejo de error si el puerto ya está en uso.
        print(f"[ERROR] No se pudo iniciar el servidor. ¿El puerto {port} está ocupado? Detalle: {e}")
        return None

# Se tomó esta decisión luego de tener problemas a la hora de testear situaciones donde el servidor se detiene,
# situación a la cual no se podria llegar teniendo multiples clientes, entonces se refactorizó el codigo para poder 
# finalizar/cerrar el servidor presionando la tecla enter.

def accept_connections(server_socket):
    """
    Este es el bucle principal que acepta conexiones.
    Ahora se ejecutará en su propio hilo para no bloquear el hilo principal.
    """
    try:
        # El bucle se detiene cuando el evento 'shutdown' se active.
        while not shutdown_event.is_set():
            # Ponemos un timeout al accept() para que no se bloquee indefinidamente.
            # Esto va a permitir que el bucle while verifique la condición de shutdown.
            server_socket.settimeout(1.0) 
            try:
                client_socket, client_address = server_socket.accept()
                
                client_thread = threading.Thread(
                    target=handle_client, 
                    args=(client_socket, client_address)
                )
                client_thread.start()
            except socket.timeout:
                continue
    except Exception as e:
        print(f"[ERROR CRÍTICO] Error en el bucle de aceptación: {e}")
    finally:
        print("[INFO] El bucle de aceptación de conexiones ha terminado.")
        server_socket.close()

def main():
    """Función principal que maneja el cierre limpio."""
    db_manager.setup_database()
    
    server_socket = init_socket(HOST, PORT)
    if not server_socket:
        return

    # Creamos y lanzamos un hilo para el bucle que acepta conexiones.
    accept_thread = threading.Thread(target=accept_connections, args=(server_socket,))
    accept_thread.start()

    print("[INFO] Servidor iniciado. Presiona Enter para detener.")
    
    # El hilo principal ahora espera a que el usuario presione Enter.
    input() # Esta es una llamada bloqueante.

    # Cuando el usuario presiona Enter, iniciamos la secuencia de apagado.
    print("\n[*] Iniciando apagado del servidor...")
    shutdown_event.set() # Activamos la bandera para detener el bucle de accept_connections.
    
    # Esperamos a que el hilo de aceptación termine limpiamente.
    accept_thread.join()
    
    print("[*] Servidor detenido correctamente.")

if __name__ == "__main__":
    main()