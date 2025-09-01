# Script del cliente

# client.py
import socket

HOST = '127.0.0.1'
PORT = 5000

def run_client():
    """Inicia y gestiona el cliente de chat."""
    
    # Crear un socket TCP/IP.
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        try:
            # Intentar conectar al servidor.
            client_socket.connect((HOST, PORT))
            print("Conectado al servidor de chat. Escribe 'éxito' para salir.")

            # Bucle para enviar mensajes.
            while True:
                # Solicitar input del usuario.
                mensaje = input("> ")
                
                # Enviar el mensaje al servidor, codificado en utf-8.
                client_socket.send(mensaje.encode('utf-8'))

                # Si el usuario escribe 'éxito', salimos del bucle.
                if mensaje.lower() == 'éxito':
                    break
                
                # Recibir la respuesta del servidor (hasta 1024 bytes).
                respuesta = client_socket.recv(1024).decode('utf-8')
                # Imprimir la respuesta del servidor.
                print(f"Servidor: {respuesta}")

        except ConnectionRefusedError:
            # Manejo de error si el servidor no está activo.
            print("[ERROR] No se pudo conectar. ¿El servidor está corriendo?")
        except Exception as e:
            # Manejo de cualquier otro error.
            print(f"[ERROR] Ocurrió un error: {e}")
        finally:
            # El 'with' se encarga de cerrar el socket automáticamente, 
            # pero un mensaje de cierre es buena práctica.
            print("Desconectado del servidor.")


if __name__ == "__main__":
    run_client()