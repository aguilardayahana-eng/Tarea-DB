from flask import request, jsonify
from models.usuariosModel import (
    obtener_usuarios, obtener_usuario,
    insertar_usuarios, insertar_usuario,
    actualizar_usuario, eliminar_usuario,
    debug_usuario
)
from bson import ObjectId
from typing import Optional, List, Dict, Any
import logging

# Configurar logging
logger = logging.getLogger(__name__)

def _validate_object_id(id_str: str) -> Optional[str]:
    """Valida si es un ObjectId válido"""
    try:
        ObjectId(id_str.strip())
        return id_str.strip()
    except:
        return None

def _get_request_data(expected_type: type) -> Optional[Any]:
    """Obtiene y valida datos del request"""
    try:
        data = request.get_json()
        if not data:
            return None
        if expected_type == list and not isinstance(data, list):
            return None
        if expected_type == dict and not isinstance(data, dict):
            return None
        return data
    except:
        return None

# =========================
# GET TODOS
# =========================
def get_usuarios():
    try:
        usuarios = obtener_usuarios()
        return jsonify(usuarios), 200
    except Exception as e:
        logger.error(f"Error obteniendo usuarios: {str(e)}")
        return jsonify({"error": "Error interno del servidor"}), 500

# =========================
# GET UNO
# =========================
def get_usuario(id: str):
    try:
        valid_id = _validate_object_id(id)
        if not valid_id:
            return jsonify({"error": "ID inválido"}), 400

        usuario = obtener_usuario(valid_id)
        if not usuario:
            return jsonify({"error": "Usuario no encontrado", "id": valid_id}), 404

        return jsonify(usuario), 200
    except Exception as e:
        logger.error(f"Error obteniendo usuario {id}: {str(e)}")
        return jsonify({"error": "Error interno del servidor"}), 500

# =========================
# POST MULTIPLE
# =========================
def crear_usuarios():
    try:
        data = _get_request_data(list)
        if not data:
            return jsonify({"error": "Se requiere un array de usuarios"}), 400

        resultado = insertar_usuarios(data)
        
        return jsonify({
            "message": "Usuarios creados exitosamente",
            "count": len(resultado.inserted_ids),
            "inserted_ids": [str(oid) for oid in resultado.inserted_ids]
        }), 201

    except Exception as e:
        logger.error(f"Error creando usuarios múltiples: {str(e)}")
        return jsonify({"error": "Error interno del servidor"}), 500

# =========================
# POST UNO
# =========================
def crear_usuario():
    try:
        data = _get_request_data(dict)
        if not data:
            return jsonify({"error": "Se requieren datos del usuario"}), 400

        resultado = insertar_usuario(data)
        
        return jsonify({
            "message": "Usuario creado exitosamente",
            "inserted_id": str(resultado.inserted_id)
        }), 201

    except Exception as e:
        logger.error(f"Error creando usuario: {str(e)}")
        return jsonify({"error": "Error interno del servidor"}), 500

# =========================
# PUT UPDATE
# =========================
def actualizar_usuario_controller(id: str):
    try:
        valid_id = _validate_object_id(id)
        if not valid_id:
            return jsonify({"error": "ID inválido"}), 400

        data = _get_request_data(dict)
        if not data:
            return jsonify({"error": "Se requieren datos para actualizar"}), 400

        resultado = actualizar_usuario(valid_id, data)
        if resultado is None:
            return jsonify({"error": "Error interno del servidor"}), 500

        matched = getattr(resultado, "matched_count", 0)
        modified = getattr(resultado, "modified_count", 0)

        if matched == 0:
            return jsonify({
                "error": "Usuario no encontrado",
                "id": valid_id
            }), 404

        return jsonify({
            "message": "Usuario actualizado exitosamente",
            "matched_count": matched,
            "modified_count": modified
        }), 200

    except Exception as e:
        logger.error(f"Error actualizando usuario {id}: {str(e)}")
        return jsonify({"error": "Error interno del servidor"}), 500

# =========================
# DELETE
# =========================
def eliminar_usuario_controller(id: str):
    try:
        valid_id = _validate_object_id(id)
        if not valid_id:
            return jsonify({"error": "ID inválido"}), 400

        resultado = eliminar_usuario(valid_id)
        if resultado.deleted_count == 0:
            return jsonify({
                "error": "Usuario no encontrado",
                "id": valid_id
            }), 404

        return jsonify({
            "message": "Usuario eliminado exitosamente",
            "deleted_count": resultado.deleted_count
        }), 200

    except Exception as e:
        logger.error(f"Error eliminando usuario {id}: {str(e)}")
        return jsonify({"error": "Error interno del servidor"}), 500

# =========================
# DEBUG
# =========================
def debug_usuario_controller(id: str):
    try:
        valid_id = _validate_object_id(id)
        if not valid_id:
            return jsonify({"error": "ID inválido"}), 400

        debug_info = debug_usuario(valid_id)
        return jsonify(debug_info), 200
    except Exception as e:
        logger.error(f"Error en debug usuario {id}: {str(e)}")
        return jsonify({"error": "Error en debug"}), 500
    