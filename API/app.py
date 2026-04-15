from flask import Flask, jsonify, request
from flask_cors import CORS

from config.db import conectar_db

from routes.ventasRoutes import ventas_bp
from routes.usuarioRoutes import usuarios_bp
from routes.marcasRoutes import marcas_bp
from routes.prendasRoutes import prendas_bp
from routes.reportes_routes import reportes_bp

app = Flask(__name__)
app.url_map.strict_slashes = False

CORS(
    app,
    resources={r"/*": {"origins": "http://localhost:4200"}},
    supports_credentials=True
)
@app.after_request
def after_request(response):
    response.headers["Access-Control-Allow-Origin"] = "http://localhost:4200"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type, Authorization"
    response.headers["Access-Control-Allow-Methods"] = "GET, POST, PUT, DELETE, OPTIONS"
    return response
# Base de datos
db = conectar_db()

# Blueprints
app.register_blueprint(ventas_bp, url_prefix="/api/ventas")
app.register_blueprint(usuarios_bp, url_prefix="/api/usuarios")
app.register_blueprint(marcas_bp, url_prefix="/api/marcas")
app.register_blueprint(prendas_bp, url_prefix="/api/prendas")
app.register_blueprint(reportes_bp, url_prefix="/api")

# Ruta principal
@app.route('/')
def index():
    return jsonify({"message": "API funcionando en puerto 3000 ✅"})

# Error 404
@app.errorhandler(404)
def not_found(e):
    return jsonify({"error": "Ruta no encontrada"}), 404


if __name__ == "__main__":
    print("🚀 Backend corriendo en http://localhost:3000")
    app.run(host="0.0.0.0", port=3000, debug=True)