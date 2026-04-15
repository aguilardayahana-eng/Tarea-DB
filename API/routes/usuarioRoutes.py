"""
Rutas completas para gestión de Usuarios
API RESTful con documentación OpenAPI/Swagger compatible
"""
from flask import Blueprint, request
from controllers.usuariosController import (
    get_usuarios,
    get_usuario,
    crear_usuarios,
    crear_usuario,
    actualizar_usuario_controller,
    eliminar_usuario_controller,
    debug_usuario_controller
)
from functools import wraps
from bson import ObjectId
import logging

logger = logging.getLogger(__name__)
usuarios_bp = Blueprint("usuarios", __name__, url_prefix="/api/v1/usuarios")

# =========================
# MIDDLEWARES / VALIDADORES
# =========================
def validar_object_id(f):
    """Middleware para validar ObjectId en parámetros de ruta"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        id_param = kwargs.get('id')
        if id_param and not ObjectId.is_valid(id_param):
            return {
                "error": "ID inválido",
                "id_recibido": id_param,
                "formato_esperado": "ObjectId MongoDB (24 caracteres hex)"
            }, 400
        return f(*args, **kwargs)
    return decorated_function

def validar_contenido_json(f):
    """Middleware para validar que el request tenga JSON válido"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not request.is_json:
            return {"error": "Content-Type debe ser application/json"}, 400
        return f(*args, **kwargs)
    return decorated_function

# =========================
# GET - LISTAR Y OBTENER
# =========================
@usuarios_bp.route("/", methods=["GET"])
def ruta_get_usuarios():
    """
    Obtiene lista de usuarios
    Parámetros de query soportados:
    ?limit=10&skip=0
    """
    return get_usuarios()

@usuarios_bp.route("/<id>", methods=["GET"])
@validar_object_id
def ruta_get_usuario(id):
    """Obtiene un usuario específico por ID"""
    return get_usuario(id)

# =========================
# POST - CREAR
# =========================
@usuarios_bp.route("/", methods=["POST"])
@validar_contenido_json
def ruta_crear_usuario():
    """
    Crea un nuevo usuario
    Body: { "nombre": "Juan", "email": "juan@email.com", ... }
    """
    return crear_usuario()

@usuarios_bp.route("/multiple", methods=["POST"])
@validar_contenido_json
def ruta_crear_usuarios():
    """
    Crea múltiples usuarios
    Body: [
        { "nombre": "Juan", "email": "juan@email.com" },
        { "nombre": "Ana", "email": "ana@email.com" }
    ]
    """
    return crear_usuarios()

# =========================
# PUT - ACTUALIZAR
# =========================
@usuarios_bp.route("/<id>", methods=["PUT"])
@validar_object_id
@validar_contenido_json
def ruta_actualizar_usuario(id):
    """Actualiza un usuario existente por ID"""
    return actualizar_usuario_controller(id)

# =========================
# DELETE - ELIMINAR
# =========================
@usuarios_bp.route("/<id>", methods=["DELETE"])
@validar_object_id
def ruta_eliminar_usuario(id):
    """Elimina un usuario por ID"""
    return eliminar_usuario_controller(id)

# =========================
# UTILIDADES ADICIONALES
# =========================
@usuarios_bp.route("/count", methods=["GET"])
def ruta_contar_usuarios():
    """Obtiene el total de usuarios en la colección"""
    from models.usuariosModel import contar_usuarios
    try:
        total = contar_usuarios()
        return {
            "total_usuarios": total,
            "message": "Conteo exitoso"
        }, 200
    except Exception as e:
        logger.error(f"Error contando usuarios: {str(e)}")
        return {"error": "Error interno"}, 500

@usuarios_bp.route("/debug/<id>", methods=["GET"])
@validar_object_id
def ruta_debug_usuario(id):
    """Debug completo de un usuario (desarrollo)"""
    return debug_usuario_controller(id)

@usuarios_bp.route("/debug", methods=["GET"])
def ruta_debug_general():
    """Información general de debug de la colección"""
    from models.usuariosModel import contar_usuarios
    try:
        return {
            "collection": "usuarios",
            "total": contar_usuarios(),
            "status": "OK",
            "timestamp": str(datetime.now())
        }, 200
    except Exception as e:
        return {"error": str(e)}, 500

# =========================
# RUTAS DE UTILIDAD (OPCIONALES)
# =========================
@usuarios_bp.route("/limpiar", methods=["DELETE"])
def ruta_limpiar_coleccion():
    """
    ⚠️ LIMPIA TODA LA COLECCIÓN (SOLO DESARROLLO)
    Requiere header: X-Dev-Key: tu_clave_secreta
    """
    dev_key = request.headers.get('X-Dev-Key')
    if dev_key != "dev-secret-2024":  # Cambia esto por tu clave
        return {"error": "Acceso denegado"}, 403
    
    from models.usuariosModel import limpiar_coleccion
    result = limpiar_coleccion()
    return result, 200

# =========================
# HEALTH CHECK
# =========================
@usuarios_bp.route("/health", methods=["GET"])
def ruta_health_check():
    """Health check de la colección de usuarios"""
    from models.usuariosModel import contar_usuarios
    try:
        count = contar_usuarios()
        return {
            "status": "healthy",
            "collection": "usuarios",
            "record_count": count,
            "timestamp": str(datetime.now())
        }, 200
    except Exception as e:
        return {
            "status": "unhealthy",
            "error": str(e)
        }, 503