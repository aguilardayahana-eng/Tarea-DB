"""
Modelo de Prendas para MongoDB
Operaciones CRUD avanzadas con filtros, validaciones y relaciones
"""
from config.db import conectar_db
from bson import ObjectId
from typing import List, Dict, Any, Optional, Union
import logging
from datetime import datetime
from pymongo import DESCENDING

logger = logging.getLogger(__name__)
db = conectar_db()
prendas_collection = db["prendas"]

def serialize_prenda(prenda: Optional[Dict[str, Any]]) -> Optional[Dict[str, Any]]:
    """Serializa una prenda (ObjectId → string)"""
    if not prenda:
        return None
    
    serialized = prenda.copy()
    if '_id' in serialized:
        serialized['_id'] = str(serialized['_id'])
    
    # Serializar IDs relacionados
    for field in ['marca_id', 'talla_id', 'color_id']:
        if field in serialized and isinstance(serialized[field], ObjectId):
            serialized[field] = str(serialized[field])
    
    return serialized

def deserialize_id(data: Dict[str, Any]) -> Dict[str, Any]:
    """Elimina _id para evitar conflictos en insert/update"""
    data_copy = data.copy()
    data_copy.pop('_id', None)
    return data_copy

# =========================
# READ OPERATIONS
# =========================
def obtener_prendas(limit: int = 50, skip: int = 0, filtro: Dict = None, 
                   sort: Dict = None) -> List[Dict[str, Any]]:
    """Obtiene prendas con filtros avanzados y paginación"""
    try:
        if filtro is None:
            filtro = {}
        
        if sort is None:
            sort = {'created_at': DESCENDING}
        
        # Filtros comunes
        query = {}
        if filtro.get('marca_id'):
            query['marca_id'] = filtro['marca_id']
        if filtro.get('categoria'):
            query['categoria'] = filtro['categoria']
        if 'activo' in filtro:
            query['activo'] = filtro['activo']
        if filtro.get('precio_min'):
            query['precio'] = {'$gte': filtro['precio_min']}
        if filtro.get('precio_max'):
            if 'precio' not in query:
                query['precio'] = {}
            query['precio']['$lte'] = filtro['precio_max']
        if filtro.get('stock_min'):
            query['stock'] = {'$gte': filtro['stock_min']}
        
        prendas = list(
            prendas_collection
            .find(query)
            .sort(sort)
            .skip(skip)
            .limit(limit)
        )
        
        return [serialize_prenda(p) for p in prendas]
    except Exception as e:
        logger.error(f"Error obteniendo prendas: {str(e)}")
        return []

def obtener_prenda(id: str) -> Optional[Dict[str, Any]]:
    """Obtiene una prenda por ID"""
    try:
        prenda = prendas_collection.find_one({"_id": ObjectId(id)})
        return serialize_prenda(prenda)
    except Exception as e:
        logger.warning(f"ID inválido o error obteniendo prenda {id}: {str(e)}")
        return None

def contar_prendas(filtro: Dict = None) -> int:
    """Cuenta prendas con filtros"""
    try:
        if filtro is None:
            return prendas_collection.count_documents({})
        
        query = {}
        if filtro.get('marca_id'):
            query['marca_id'] = filtro['marca_id']
        if filtro.get('categoria'):
            query['categoria'] = filtro['categoria']
        if 'activo' in filtro:
            query['activo'] = filtro['activo']
            
        return prendas_collection.count_documents(query)
    except Exception as e:
        logger.error(f"Error contando prendas: {str(e)}")
        return 0

# =========================
# CREATE OPERATIONS
# =========================
def insertar_prendas(data: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Inserta múltiples prendas"""
    try:
        if not data or not isinstance(data, list):
            raise ValueError("Data debe ser lista no vacía")
        
        normalized_data = []
        for item in data:
            normalized = _normalize_prenda_data(item)
            normalized_data.append(normalized)
        
        result = prendas_collection.insert_many(normalized_data)
        logger.info(f"Insertadas {len(result.inserted_ids)} prendas")
        return result
    except Exception as e:
        logger.error(f"Error insertando prendas múltiples: {str(e)}")
        raise

def insertar_prenda(data: Dict[str, Any]) -> Dict[str, Any]:
    """Inserta una prenda"""
    try:
        if not isinstance(data, dict):
            raise ValueError("Data debe ser diccionario")
        
        normalized = _normalize_prenda_data(data)
        result = prendas_collection.insert_one(normalized)
        logger.info(f"Prenda insertada: {str(result.inserted_id)}")
        return result
    except Exception as e:
        logger.error(f"Error insertando prenda: {str(e)}")
        raise

def _normalize_prenda_data(data: Dict[str, Any]) -> Dict[str, Any]:
    """Normaliza datos de prenda con valores por defecto"""
    normalized = deserialize_id(data)
    
    # Campos obligatorios
    normalized.setdefault('nombre', 'Sin nombre')
    normalized.setdefault('marca_id', '')
    normalized.setdefault('categoria', 'General')
    
    # Campos numéricos con defaults
    normalized.setdefault('precio', 0.0)
    normalized.setdefault('stock', 0)
    normalized.setdefault('talla', 'M')
    
    # Booleans
    normalized.setdefault('activo', True)
    normalized.setdefault('novedad', False)
    
    # Timestamps
    now = datetime.utcnow()
    normalized.setdefault('created_at', now)
    normalized.setdefault('updated_at', now)
    
    return normalized

# =========================
# UPDATE OPERATIONS
# =========================
def actualizar_prenda(id: str, data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """Actualiza prenda por ID"""
    try:
        ObjectId(id)
        
        update_data = deserialize_id(data)
        update_data['updated_at'] = datetime.utcnow()
        
        result = prendas_collection.update_one(
            {"_id": ObjectId(id)},
            {"$set": update_data}
        )
        
        if result.matched_count == 0:
            logger.warning(f"Prenda no encontrada: {id}")
            return None
        
        logger.info(f"Prenda actualizada: {id}")
        return result
    except Exception as e:
        logger.error(f"Error actualizando prenda {id}: {str(e)}")
        return None

# =========================
# DELETE OPERATIONS
# =========================
def eliminar_prenda(id: str) -> Optional[Dict[str, Any]]:
    """Elimina prenda por ID"""
    try:
        ObjectId(id)
        result = prendas_collection.delete_one({"_id": ObjectId(id)})
        
        if result.deleted_count == 0:
            logger.warning(f"Prenda no encontrada para eliminar: {id}")
            return None
        
        logger.info(f"Prenda eliminada: {id}")
        return result
    except Exception as e:
        logger.error(f"Error eliminando prenda {id}: {str(e)}")
        return None

# =========================
# QUERIES AVANZADAS
# =========================
def prendas_por_marca(marca_id: str, limit: int = 20) -> List[Dict[str, Any]]:
    """Prendas filtradas por marca"""
    try:
        ObjectId(marca_id)
        return obtener_prendas(
            limit=limit, 
            filtro={'marca_id': marca_id},
            sort={'created_at': DESCENDING}
        )
    except:
        return []

def prendas_en_stock(limit: int = 50) -> List[Dict[str, Any]]:
    """Prendas con stock > 0"""
    return obtener_prendas(
        limit=limit,
        filtro={'stock': {'$gt': 0}},
        sort={'stock': DESCENDING}
    )

def prendas_novedad(limit: int = 10) -> List[Dict[str, Any]]:
    """Prendas marcadas como novedad"""
    return obtener_prendas(
        limit=limit,
        filtro={'novedad': True},
        sort={'created_at': DESCENDING}
    )

def estadisticas_prendas() -> Dict[str, Any]:
    """Estadísticas generales de prendas"""
    try:
        pipeline = [
            {"$group": {
                "_id": "$categoria",
                "count": {"$sum": 1},
                "stock_total": {"$sum": "$stock"},
                "precio_promedio": {"$avg": "$precio"}
            }},
            {"$sort": {"count": DESCENDING}}
        ]
        stats = list(prendas_collection.aggregate(pipeline))
        total_prendas = contar_prendas()
        
        return {
            "total_prendas": total_prendas,
            "por_categoria": stats,
            "ultima_actualizacion": datetime.utcnow().isoformat()
        }
    except Exception as e:
        logger.error(f"Error en estadísticas: {str(e)}")
        return {"error": "No disponible"}

# =========================
# UTILIDADES Y DEBUG
# =========================
def prenda_existe(id: str) -> bool:
    """Verifica existencia por ID"""
    try:
        return prendas_collection.count_documents({"_id": ObjectId(id)}) > 0
    except:
        return False

def debug_prenda(id: str) -> Dict[str, Any]:
    """Debug completo de prenda"""
    try:
        ObjectId(id)
        prenda = prendas_collection.find_one({"_id": ObjectId(id)})
        return {
            "debug_info": {
                "id_valid": True,
                "exists": prenda is not None,
                "total_prendas": contar_prendas()
            },
            "prenda": serialize_prenda(prenda)
        }
    except Exception as e:
        return {"debug_info": {"id_valid": False, "error": str(e)}}

def limpiar_coleccion_prendas() -> Dict[str, Any]:
    """⚠️ LIMPIAR COLECCIÓN (DESARROLLO)"""
    try:
        result = prendas_collection.delete_many({})
        return {"message": f"Limpiada {result.deleted_count} prendas"}
    except Exception as e:
        return {"error": str(e)}