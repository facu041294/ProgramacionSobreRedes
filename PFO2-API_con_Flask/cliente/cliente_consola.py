# El script del cliente
# cliente/cliente_consola.py

import requests
import getpass # Librería para pedir contraseñas sin que se vean en la terminal.

# La URL base de nuestra API. La definimos aquí para no repetirla.
BASE_URL = "http://localhost:5000"

def registrar_usuario():
    """Función para manejar el flujo de registro de un nuevo usuario."""
    print("\n--- Registro de Nuevo Usuario ---")
    usuario = input("Ingrese su nombre de usuario: ")
    # getpass.getpass() oculta la entrada de la contraseña.
    password = getpass.getpass("Ingrese su contraseña: ")

    # El 'payload' que enviaremos a la API, en formato de diccionario.
    payload = {"usuario": usuario, "contraseña": password}
    
    try:
        # Hacemos la petición POST al endpoint /registro.
        response = requests.post(f"{BASE_URL}/registro", json=payload)
        
        # requests nos permite chequear si la respuesta fue exitosa (código 2xx).
        if response.status_code == 201:
            print("\n[ÉXITO] Usuario registrado correctamente.")
        else:
            # Si no, mostramos el error que nos devuelve la API.
            error_msg = response.json().get("error", "Error desconocido.")
            print(f"\n[ERROR] No se pudo registrar: {error_msg}")
    
    except requests.exceptions.ConnectionError:
        print("\n[ERROR CRÍTICO] No se pudo conectar con el servidor. ¿Está corriendo?")

def iniciar_sesion():
    """Función para manejar el flujo de inicio de sesión."""
    print("\n--- Inicio de Sesión ---")
    usuario = input("Usuario: ")
    password = getpass.getpass("Contraseña: ")
    
    payload = {"usuario": usuario, "contraseña": password}

    try:
        response = requests.post(f"{BASE_URL}/login", json=payload)

        if response.ok: # .ok es un booleano para códigos de estado 2xx.
            print("\n[ÉXITO] Inicio de sesión correcto.")
            # Si el login es exitoso, damos acceso a las tareas.
            acceder_a_tareas()
        else:
            error_msg = response.json().get("error", "Error desconocido.")
            print(f"\n[ERROR] Credenciales inválidas: {error_msg}")
    
    except requests.exceptions.ConnectionError:
        print("\n[ERROR CRÍTICO] No se pudo conectar con el servidor.")

def acceder_a_tareas():
    """
    Función que accede al endpoint protegido '/tareas'.
    En una app real, aquí enviaríamos un token de autenticación.
    """
    print("\nAccediendo a la zona de tareas...")
    try:
        response = requests.get(f"{BASE_URL}/tareas")
        
        if response.ok:
            # El endpoint /tareas devuelve HTML. Lo imprimimos.
            # No es lo ideal para una consola, pero cumple con la consigna.
            print("\n--- Contenido de Tareas ---")
            print(response.text) # .text nos da el body de la respuesta como string.
            print("--------------------------")
        else:
            print("\n[ERROR] No se pudo acceder a la zona de tareas.")
    
    except requests.exceptions.ConnectionError:
        print("\n[ERROR CRÍTICO] No se pudo conectar con el servidor.")


def menu_principal():
    """El bucle principal que muestra el menú y gestiona la interacción."""
    while True:
        print("\n===== MENÚ PRINCIPAL =====")
        print("1. Registrarse")
        print("2. Iniciar Sesión")
        print("3. Salir")
        
        opcion = input("Seleccione una opción: ")

        if opcion == '1':
            registrar_usuario()
        elif opcion == '2':
            iniciar_sesion()
        elif opcion == '3':
            print("Saliendo del programa.")
            break
        else:
            print("Opción no válida. Por favor, intente de nuevo.")

if __name__ == "__main__":
    menu_principal()