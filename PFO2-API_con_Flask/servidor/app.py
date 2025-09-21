# El corazón de la aplicación Flask (rutas y lógica) 
# servidor/app.py

# Importamos las clases y funciones necesarias de Flask y de nuestros módulos.
from flask import Flask, request, jsonify, render_template
from . import auth         # El '.' indica que importamos desde el mismo paquete (servidor)
from . import database

# Inicializamos la aplicación Flask.
app = Flask(__name__)

# --- INICIALIZACIÓN ---
# Nos aseguramos de que la base de datos y sus tablas estén creadas al iniciar la app.
database.inicializar_db()

# --- ENDPOINTS DE LA API ---

@app.route('/registro', methods=['POST'])
def registro():
    """
    Endpoint para registrar un nuevo usuario.
    Recibe un JSON con 'usuario' y 'contraseña'.
    """
    # 1. Obtenemos los datos del request. request.get_json() parsea el body.
    datos = request.get_json()
    usuario = datos.get('usuario')
    password = datos.get('contraseña')

    # 2. Validación básica de entrada.
    if not usuario or not password:
        return jsonify({"error": "Usuario y contraseña son requeridos"}), 400

    # 3. Hasheamos la contraseña ANTES de guardarla.
    password_hash = auth.hashear_password(password)

    # 4. Intentamos crear el usuario en la base de datos.
    if database.crear_usuario(usuario, password_hash):
        # Si fue exitoso, devolvemos un código 201 (Created).
        return jsonify({"mensaje": "Usuario registrado exitosamente"}), 201
    else:
        # Si falla (ej. usuario ya existe), devolvemos un 409 (Conflict).
        return jsonify({"error": "El nombre de usuario ya existe"}), 409

@app.route('/login', methods=['POST'])
def login():
    """
    Endpoint para iniciar sesión.
    Recibe un JSON con 'usuario' y 'contraseña'.
    """
    # 1. Obtenemos los datos del request.
    datos = request.get_json()
    usuario_nombre = datos.get('usuario')
    password_plano = datos.get('contraseña')

    # 2. Validación básica.
    if not usuario_nombre or not password_plano:
        return jsonify({"error": "Usuario y contraseña son requeridos"}), 400

    # 3. Buscamos al usuario en la base de datos.
    usuario_db = database.obtener_usuario(usuario_nombre)

    # 4. Verificamos si el usuario existe Y si la contraseña es correcta.
    # Usamos la función de auth para comparar la contraseña plana con el hash.
    if usuario_db and auth.verificar_password(usuario_db['password_hash'], password_plano):
        # En una app real, leí en foros que aquí se deberia generar un token JWT. Para la PFO, solo damos acceso.
        return jsonify({"mensaje": f"Login exitoso. Bienvenido {usuario_nombre}!"})
    else:
        # Si el usuario no existe o la contraseña es incorrecta, devolvemos 401 (Unauthorized).
        return jsonify({"error": "Credenciales inválidas"}), 401

@app.route('/tareas', methods=['GET'])
def mostrar_tareas():
    """
    Endpoint de bienvenida. En un contexto real, estaría protegido
    y solo sería accesible después de un login exitoso.
    """
    # Flask buscará este archivo en la carpeta 'templates/'.
    return render_template('bienvenida.html')

# --- EJECUCIÓN DEL SERVIDOR ---

if __name__ == '__main__':
    # El debug=True es útil para desarrollo, ya que reinicia el servidor automáticamente
    # con cada cambio. NUNCA se usa en producción.
    app.run(debug=True, port=5000)