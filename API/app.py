from flask import Flask, jsonify
from config.db import conectar_db

# Importar todos los blueprints
from routes.ventasRoutes import ventas_bp
from routes.usuarioRoutes import usuarios_bp
from routes.marcasRoutes import marcas_bp
from routes.prendasRoutes import prendas_bp

# Crear la app Flask
app = Flask(__name__)

# Configuración opcional
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True

# Conectar a la base de datos al iniciar
db = conectar_db()

# Registrar rutas (blueprints)
app.register_blueprint(ventas_bp, url_prefix="/api/ventas")
app.register_blueprint(usuarios_bp, url_prefix="/api/usuarios")
app.register_blueprint(marcas_bp, url_prefix="/api/marcas")
app.register_blueprint(prendas_bp, url_prefix="/api/prendas")
from routes.reportes_routes import reportes_bp
app.register_blueprint(reportes_bp, url_prefix="/api")
def index():
    return jsonify({"message": "API Tienda Ropa funcionando"})

# Manejo de errores 404
@app.errorhandler(404)
def not_found(e):
    return jsonify({"error": "Ruta no encontrada"}), 404

# Ejecutar servidor
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000, debug=True)