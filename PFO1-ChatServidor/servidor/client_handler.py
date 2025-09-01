# Lógica para manejar un cliente (con hilos)

# client_handler.py
from datetime import datetime
from . import db_manager # Importamos nuestro módulo de base de datos

def handle_client(client_socket, client_address):
    """
    Esta función se ejecuta en un hilo separado para cada cliente conectado.
    """
    print(f"[NUEVA CONEXIÓN] {client_address} conectado.")
    ip_cliente = client_address[0] # La dirección IP del cliente

    try:
        # Bucle principal para recibir datos del cliente.
        while True:
            # Espera a recibir datos (hasta 1024 bytes). recv() es bloqueante.
            msg = client_socket.recv(1024).decode('utf-8')
            
            # Si no se recibe mensaje, el cliente se desconectó.
            if not msg:
                break 
            
            # Si el cliente escribe "éxito", terminamos la conexión.
            if msg.lower() == 'éxito':
                print(f"[DESCONEXIÓN] {client_address} ha terminado la sesión.")
                break

            print(f"[{client_address}] Mensaje recibido: {msg}")
            
            # Guardamos el mensaje en la base de datos.
            if db_manager.guardar_mensaje(msg, ip_cliente):
                # Si se guardó correctamente, preparamos la confirmación.
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                respuesta = f"Mensaje recibido: <{timestamp}>"
            else:
                # Si hubo un error en la DB, se lo informamos al cliente.
                respuesta = "Error: No se pudo guardar tu mensaje."
            
            # Enviamos la respuesta de vuelta al cliente.
            client_socket.send(respuesta.encode('utf-8'))

    except ConnectionResetError:
        # Esto ocurre si el cliente cierra la conexión de forma abrupta.
        print(f"[CONEXIÓN PERDIDA] {client_address} se desconectó inesperadamente.")
    except Exception as e:
        # Capturamos cualquier otro error inesperado.
        print(f"[ERROR] Ocurrió un error con {client_address}: {e}")
    finally:
        # Este bloque se ejecuta siempre, sin importar cómo salió del try.
        # Es crucial para asegurarnos de que el socket del cliente se cierre.
        client_socket.close()