"""
Rutas completas para gestión de Marcas
API RESTful con validaciones, documentación y utilidades
"""
from flask import Blueprint, request
from controllers.marcasController import (
    get_marcas, get_marca, crear_marcas, crear_marca,
    actualizar_marca_controller, eliminar_marca_controller, get_count_marcas
)
from models.marcasModel import (
    buscar_marcas, debug_marca, limpiar_coleccion_marcas
)
from functools import wraps
from bson import ObjectId
from datetime import datetime
import logging

logger = logging.getLogger(__name__)
marcas_bp = Blueprint("marcas", __name__, url_prefix="/api/v1/marcas")

# =========================
# MIDDLEWARES / VALIDADORES
# =========================
def validar_object_id(f):
    """Valida ObjectId en parámetros de ruta"""
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
    """Valida Content-Type application/json"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not request.is_json:
            return {"error": "Content-Type debe ser application/json"}, 400
        return f(*args, **kwargs)
    return decorated_function

# =========================
# GET - LISTAR Y OBTENER
# =========================
@marcas_bp.route("/", methods=["GET"])
def ruta_get_marcas():
    """
    Lista todas las marcas
    Query params:
    ?limit=10&skip=0&search=nike
    """
    return get_marcas()

@marcas_bp.route("/<id>", methods=["GET"])
@validar_object_id
def ruta_get_marca(id):
    """Obtiene una marca específica por ID"""
    return get_marca(id)

# =========================
# POST - CREAR
# =========================
@marcas_bp.route("/", methods=["POST"])
@validar_contenido_json
def ruta_crear_marca():
    """
    Crea una nueva marca
    Body: { "nombre": "Nike", "pais": "USA", "activa": true }
    """
    return crear_marca()

@marcas_bp.route("/multiple", methods=["POST"])
@validar_contenido_json
def ruta_crear_marcas():
    """
    Crea múltiples marcas
    Body: [{ "nombre": "Nike", "pais": "USA" }, { "nombre": "Adidas" }]
    """
    return crear_marcas()

# =========================
# PUT - ACTUALIZAR
# =========================
@marcas_bp.route("/<id>", methods=["PUT"])
@validar_object_id
@validar_contenido_json
def ruta_actualizar_marca(id):
    """Actualiza una marca por ID"""
    return actualizar_marca_controller(id)

# =========================
# DELETE - ELIMINAR
# =========================
@marcas_bp.route("/<id>", methods=["DELETE"])
@validar_object_id
def ruta_eliminar_marca(id):
    """Elimina una marca por ID"""
    return eliminar_marca_controller(id)

# =========================
# UTILIDADES BÁSICAS
# =========================
@marcas_bp.route("/count", methods=["GET"])
def ruta_contar_marcas():
    """Conteo total de marcas"""
    return get_count_marcas()

@marcas_bp.route("/search", methods=["GET"])
def ruta_buscar_marcas():
    """
    Busca marcas por nombre
    ?q=nike&limit=10
    """
    try:
        query = request.args.get('q', '').strip()
        limit = request.args.get('limit', 10, type=int)
        
        if not query:
            return {"error": "Parámetro 'q' requerido"}, 400
        
        resultados = buscar_marcas(query, limit)
        return {
            "query": query,
            "results": resultados,
            "limit": limit,
            "count": len(resultados)
        }, 200
    except Exception as e:
        logger.error(f"Error buscando marcas: {str(e)}")
        return {"error": "Error interno"}, 500

# =========================
# DEBUG Y DESARROLLO
# =========================
@marcas_bp.route("/debug/<id>", methods=["GET"])
@validar_object_id
def ruta_debug_marca(id):
    """Debug completo de una marca"""
    return debug_marca(id), 200

@marcas_bp.route("/debug", methods=["GET"])
def ruta_debug_general():
    """Debug general de la colección"""
    from models.marcasModel import contar_marcas
    try:
        return {
            "collection": "marcas",
            "total": contar_marcas(),
            "status": "OK",
            "timestamp": str(datetime.now())
        }, 200
    except Exception as e:
        return {"error": str(e)}, 500

# =========================
# MANTENIMIENTO (PROTEGIDO)
# =========================
@marcas_bp.route("/limpiar", methods=["DELETE"])
def ruta_limpiar_coleccion():
    """
    ⚠️ LIMPIA TODA LA COLECCIÓN (SOLO DESARROLLO)
    Header: X-Dev-Key: dev-secret-2024
    """
    dev_key = request.headers.get('X-Dev-Key')
    if dev_key != "dev-secret-2024":  # Cambia por tu clave
        return {"error": "Acceso denegado"}, 403
    
    result = limpiar_coleccion_marcas()
    return result, 200

# =========================
# HEALTH CHECK
# =========================
@marcas_bp.route("/health", methods=["GET"])
def ruta_health_check():
    """Health check de la colección de marcas"""
    from models.marcasModel import contar_marcas
    try:
        count = contar_marcas()
        return {
            "status": "healthy",
            "collection": "marcas",
            "record_count": count,
            "timestamp": str(datetime.now())
        }, 200
    except Exception as e:
        return {
            "status": "unhealthy",
            "error": str(e)
        }, 503