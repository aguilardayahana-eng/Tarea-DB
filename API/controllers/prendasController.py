from flask import request, jsonify
from models.prendasModel import (
    obtener_prendas, obtener_prenda,
    insertar_prendas, insertar_prenda,
    actualizar_prenda, eliminar_prenda,
    contar_prendas
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
def get_prendas():
    """Obtiene todas las prendas con filtros y paginación"""
    try:
        # Parámetros de query
        limit = request.args.get('limit', 50, type=int)
        skip = request.args.get('skip', 0, type=int)
        marca_id = request.args.get('marca')
        categoria = request.args.get('categoria')
        activo = request.args.get('activo', None)
        
        # Filtros opcionales
        filtro = {}
        if marca_id:
            filtro['marca_id'] = marca_id
        if categoria:
            filtro['categoria'] = categoria
        if activo is not None:
            filtro['activo'] = activo.lower() == 'true'
        
        prendas = obtener_prendas(limit=limit, skip=skip, filtro=filtro)
        total = contar_prendas(filtro)
        
        return jsonify({
            "prendas": prendas,
            "pagination": {
                "limit": limit,
                "skip": skip,
                "total": total,
                "pages": (total + limit - 1) // limit
            },
            "filtros": filtro
        }), 200
    except Exception as e:
        logger.error(f"Error obteniendo prendas: {str(e)}")
        return jsonify({"error": "Error interno del servidor"}), 500

# =========================
# GET UNO
# =========================
def get_prenda(id: str):
    """Obtiene una prenda específica por ID"""
    try:
        valid_id = _validate_object_id(id)
        if not valid_id:
            return jsonify({"error": "ID inválido"}), 400

        prenda = obtener_prenda(valid_id)
        if not prenda:
            return jsonify({"error": "Prenda no encontrada", "id": valid_id}), 404

        return jsonify(prenda), 200
    except Exception as e:
        logger.error(f"Error obteniendo prenda {id}: {str(e)}")
        return jsonify({"error": "Error interno del servidor"}), 500

# =========================
# POST MULTIPLE
# =========================
def crear_prendas():
    """Crea múltiples prendas"""
    try:
        data = _get_request_data(list)
        if not data:
            return jsonify({"error": "Se requiere un array de prendas"}), 400

        resultado = insertar_prendas(data)
        
        return jsonify({
            "message": "Prendas creadas exitosamente",
            "count": len(resultado.inserted_ids),
            "inserted_ids": [str(oid) for oid in resultado.inserted_ids]
        }), 201

    except Exception as e:
        logger.error(f"Error creando prendas múltiples: {str(e)}")
        return jsonify({"error": "Error interno del servidor"}), 500

# =========================
# POST UNO
# =========================
def crear_prenda():
    """Crea una nueva prenda"""
    try:
        data = _get_request_data(dict)
        if not data:
            return jsonify({"error": "Se requieren datos de la prenda"}), 400

        # Validaciones específicas
        if not data.get('nombre') or not data.get('marca_id'):
            return jsonify({"error": "Se requiere 'nombre' y 'marca_id'"}), 400

        resultado = insertar_prenda(data)
        
        return jsonify({
            "message": "Prenda creada exitosamente",
            "inserted_id": str(resultado.inserted_id),
            "prenda": obtener_prenda(str(resultado.inserted_id))
        }), 201

    except Exception as e:
        logger.error(f"Error creando prenda: {str(e)}")
        return jsonify({"error": "Error interno del servidor"}), 500

# =========================
# PUT UPDATE
# =========================
def actualizar_prenda_controller(id: str):
    """Actualiza una prenda existente"""
    try:
        valid_id = _validate_object_id(id)
        if not valid_id:
            return jsonify({"error": "ID inválido"}), 400

        data = _get_request_data(dict)
        if not data:
            return jsonify({"error": "Se requieren datos para actualizar"}), 400

        resultado = actualizar_prenda(valid_id, data)
        if resultado is None:
            return jsonify({"error": "Error interno del servidor"}), 500

        matched = getattr(resultado, "matched_count", 0)
        modified = getattr(resultado, "modified_count", 0)

        if matched == 0:
            return jsonify({
                "error": "Prenda no encontrada",
                "id": valid_id
            }), 404

        # Retornar prenda actualizada
        prenda_actualizada = obtener_prenda(valid_id)
        
        return jsonify({
            "message": "Prenda actualizada exitosamente",
            "matched_count": matched,
            "modified_count": modified,
            "prenda": prenda_actualizada
        }), 200

    except Exception as e:
        logger.error(f"Error actualizando prenda {id}: {str(e)}")
        return jsonify({"error": "Error interno del servidor"}), 500

# =========================
# DELETE
# =========================
def eliminar_prenda_controller(id: str):
    """Elimina una prenda por ID"""
    try:
        valid_id = _validate_object_id(id)
        if not valid_id:
            return jsonify({"error": "ID inválido"}), 400

        resultado = eliminar_prenda(valid_id)
        if resultado is None or getattr(resultado, 'deleted_count', 0) == 0:
            return jsonify({
                "error": "Prenda no encontrada",
                "id": valid_id
            }), 404

        return jsonify({
            "message": "Prenda eliminada exitosamente",
            "deleted_count": getattr(resultado, 'deleted_count', 1)
        }), 200

    except Exception as e:
        logger.error(f"Error eliminando prenda {id}: {str(e)}")
        return jsonify({"error": "Error interno del servidor"}), 500

# =========================
# UTILIDADES ESPECÍFICAS
# =========================
def get_count_prendas():
    """Obtiene conteo de prendas con filtros"""
    try:
        marca = request.args.get('marca')
        categoria = request.args.get('categoria')
        activo = request.args.get('activo')
        
        filtro = {}
        if marca: filtro['marca_id'] = marca
        if categoria: filtro['categoria'] = categoria
        if activo is not None: filtro['activo'] = activo.lower() == 'true'
        
        total = contar_prendas(filtro)
        return jsonify({
            "total_prendas": total,
            "filtros": filtro
        }), 200
    except Exception as e:
        logger.error(f"Error contando prendas: {str(e)}")
        return jsonify({"error": "Error interno"}), 500

def get_prendas_por_marca(marca_id: str):
    """Obtiene prendas de una marca específica"""
    try:
        valid_id = _validate_object_id(marca_id)
        if not valid_id:
            return jsonify({"error": "ID de marca inválido"}), 400

        prendas = obtener_prendas(filtro={'marca_id': valid_id})
        return jsonify({
            "marca_id": valid_id,
            "prendas": prendas,
            "count": len(prendas)
        }), 200
    except Exception as e:
        logger.error(f"Error obteniendo prendas por marca {marca_id}: {str(e)}")
        return jsonify({"error": "Error interno"}), 500