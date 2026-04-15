from flask import request, jsonify
from models.marcasModel import (
    obtener_marcas, obtener_marca,
    insertar_marcas, insertar_marca,
    actualizar_marca, eliminar_marca,
    contar_marcas
)
from bson import ObjectId
from typing import Optional, List, Dict, Any
import logging

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
def get_marcas():
    """Obtiene todas las marcas con paginación opcional"""
    try:
        limit = request.args.get('limit', 100, type=int)
        skip = request.args.get('skip', 0, type=int)
        
        marcas = obtener_marcas(limit=limit, skip=skip)
        return jsonify({
            "marcas": marcas,
            "limit": limit,
            "skip": skip,
            "total": contar_marcas()
        }), 200
    except Exception as e:
        logger.error(f"Error obteniendo marcas: {str(e)}")
        return jsonify({"error": "Error interno del servidor"}), 500

# =========================
# GET UNO
# =========================
def get_marca(id: str):
    """Obtiene una marca específica por ID"""
    try:
        valid_id = _validate_object_id(id)
        if not valid_id:
            return jsonify({"error": "ID inválido"}), 400

        marca = obtener_marca(valid_id)
        if not marca:
            return jsonify({"error": "Marca no encontrada", "id": valid_id}), 404

        return jsonify(marca), 200
    except Exception as e:
        logger.error(f"Error obteniendo marca {id}: {str(e)}")
        return jsonify({"error": "Error interno del servidor"}), 500

# =========================
# POST MULTIPLE
# =========================
def crear_marcas():
    """Crea múltiples marcas"""
    try:
        data = _get_request_data(list)
        if not data:
            return jsonify({"error": "Se requiere un array de marcas"}), 400

        resultado = insertar_marcas(data)
        
        return jsonify({
            "message": "Marcas creadas exitosamente",
            "count": len(resultado.inserted_ids),
            "inserted_ids": [str(oid) for oid in resultado.inserted_ids]
        }), 201

    except Exception as e:
        logger.error(f"Error creando marcas múltiples: {str(e)}")
        return jsonify({"error": "Error interno del servidor"}), 500

# =========================
# POST UNO
# =========================
def crear_marca():
    """Crea una nueva marca"""
    try:
        data = _get_request_data(dict)
        if not data:
            return jsonify({"error": "Se requieren datos de la marca"}), 400

        resultado = insertar_marca(data)
        
        return jsonify({
            "message": "Marca creada exitosamente",
            "inserted_id": str(resultado.inserted_id)
        }), 201

    except Exception as e:
        logger.error(f"Error creando marca: {str(e)}")
        return jsonify({"error": "Error interno del servidor"}), 500

# =========================
# PUT UPDATE
# =========================
def actualizar_marca_controller(id: str):
    """Actualiza una marca existente"""
    try:
        valid_id = _validate_object_id(id)
        if not valid_id:
            return jsonify({"error": "ID inválido"}), 400

        data = _get_request_data(dict)
        if not data:
            return jsonify({"error": "Se requieren datos para actualizar"}), 400

        resultado = actualizar_marca(valid_id, data)
        if resultado is None:
            return jsonify({"error": "Error interno del servidor"}), 500

        matched = getattr(resultado, "matched_count", 0)
        modified = getattr(resultado, "modified_count", 0)

        if matched == 0:
            return jsonify({
                "error": "Marca no encontrada",
                "id": valid_id
            }), 404

        return jsonify({
            "message": "Marca actualizada exitosamente",
            "matched_count": matched,
            "modified_count": modified
        }), 200

    except Exception as e:
        logger.error(f"Error actualizando marca {id}: {str(e)}")
        return jsonify({"error": "Error interno del servidor"}), 500

# =========================
# DELETE
# =========================
def eliminar_marca_controller(id: str):
    """Elimina una marca por ID"""
    try:
        valid_id = _validate_object_id(id)
        if not valid_id:
            return jsonify({"error": "ID inválido"}), 400

        resultado = eliminar_marca(valid_id)
        if resultado is None or getattr(resultado, 'deleted_count', 0) == 0:
            return jsonify({
                "error": "Marca no encontrada",
                "id": valid_id
            }), 404

        return jsonify({
            "message": "Marca eliminada exitosamente",
            "deleted_count": getattr(resultado, 'deleted_count', 1)
        }), 200

    except Exception as e:
        logger.error(f"Error eliminando marca {id}: {str(e)}")
        return jsonify({"error": "Error interno del servidor"}), 500

# =========================
# UTILIDADES EXTRA
# =========================
def get_count_marcas():
    """Obtiene el conteo total de marcas"""
    try:
        total = contar_marcas()
        return jsonify({
            "total_marcas": total,
            "message": "Conteo exitoso"
        }), 200
    except Exception as e:
        logger.error(f"Error contando marcas: {str(e)}")
        return jsonify({"error": "Error interno"}), 500