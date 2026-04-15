"""
Modelo de Marcas para MongoDB
Operaciones CRUD completas con validaciones, serialización y utilidades
"""
from config.db import conectar_db
from bson import ObjectId
from typing import List, Dict, Any, Optional
import logging
from datetime import datetime

logger = logging.getLogger(__name__)
db = conectar_db()
marcas_collection = db["marcas"]

def serialize_marca(marca: Optional[Dict[str, Any]]) -> Optional[Dict[str, Any]]:
    """Serializa una marca convirtiendo ObjectId a string"""
    if not marca:
        return None
    
    serialized = marca.copy()
    if '_id' in serialized:
        serialized['_id'] = str(serialized['_id'])
    
    # Serializar otros ObjectId si existen
    for key, value in serialized.items():
        if isinstance(value, ObjectId):
            serialized[key] = str(value)
    
    return serialized

def deserialize_id(data: Dict[str, Any]) -> Dict[str, Any]:
    """Elimina _id del data para evitar conflictos"""
    data_copy = data.copy()
    data_copy.pop('_id', None)
    return data_copy

# =========================
# READ OPERATIONS
# =========================
def obtener_marcas(limit: int = 100, skip: int = 0) -> List[Dict[str, Any]]:
    """Obtiene lista de marcas con paginación"""
    try:
        marcas = list(marcas_collection.find().skip(skip).limit(limit))
        return [serialize_marca(m) for m in marcas]
    except Exception as e:
        logger.error(f"Error obteniendo marcas: {str(e)}")
        return []

def obtener_marca(id: str) -> Optional[Dict[str, Any]]:
    """Obtiene una marca por ID"""
    try:
        marca = marcas_collection.find_one({"_id": ObjectId(id)})
        return serialize_marca(marca)
    except Exception as e:
        logger.warning(f"ID inválido o error obteniendo marca {id}: {str(e)}")
        return None

def obtener_marca_por_nombre(nombre: str) -> Optional[Dict[str, Any]]:
    """Obtiene marca por nombre (case insensitive)"""
    try:
        marca = marcas_collection.find_one({
            "nombre": {"$regex": nombre, "$options": "i"}
        })
        return serialize_marca(marca)
    except Exception as e:
        logger.error(f"Error buscando marca por nombre '{nombre}': {str(e)}")
        return None

def contar_marcas() -> int:
    """Cuenta total de marcas"""
    try:
        return marcas_collection.count_documents({})
    except Exception as e:
        logger.error(f"Error contando marcas: {str(e)}")
        return 0

# =========================
# CREATE OPERATIONS
# =========================
def insertar_marcas(data: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Inserta múltiples marcas"""
    try:
        if not data or not isinstance(data, list):
            raise ValueError("Data debe ser una lista no vacía")
        
        normalized_data = []
        for item in data:
            normalized = deserialize_id(item)
            if 'created_at' not in normalized:
                normalized['created_at'] = datetime.utcnow()
            if 'nombre' not in normalized:
                raise ValueError("Cada marca debe tener 'nombre'")
            normalized_data.append(normalized)
        
        result = marcas_collection.insert_many(normalized_data)
        logger.info(f"Insertadas {len(result.inserted_ids)} marcas")
        return result
    except Exception as e:
        logger.error(f"Error insertando marcas múltiples: {str(e)}")
        raise

def insertar_marca(data: Dict[str, Any]) -> Dict[str, Any]:
    """Inserta una sola marca"""
    try:
        if not isinstance(data, dict) or 'nombre' not in data:
            raise ValueError("Data debe ser un diccionario con 'nombre'")
        
        normalized = deserialize_id(data)
        if 'created_at' not in normalized:
            normalized['created_at'] = datetime.utcnow()
        if 'updated_at' not in normalized:
            normalized['updated_at'] = datetime.utcnow()
        
        result = marcas_collection.insert_one(normalized)
        logger.info(f"Marca insertada con ID: {str(result.inserted_id)}")
        return result
    except Exception as e:
        logger.error(f"Error insertando marca: {str(e)}")
        raise

# =========================
# UPDATE OPERATIONS
# =========================
def actualizar_marca(id: str, data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """Actualiza una marca por ID"""
    try:
        ObjectId(id)  # Validar ID
        
        update_data = deserialize_id(data)
        update_data['updated_at'] = datetime.utcnow()
        
        result = marcas_collection.update_one(
            {"_id": ObjectId(id)},
            {"$set": update_data}
        )
        
        if result.matched_count == 0:
            logger.warning(f"Marca no encontrada para actualizar: {id}")
            return None
        
        logger.info(f"Marca actualizada: {id}")
        return result
        
    except Exception as e:
        logger.error(f"Error actualizando marca {id}: {str(e)}")
        return None

# =========================
# DELETE OPERATIONS
# =========================
def eliminar_marca(id: str) -> Optional[Dict[str, Any]]:
    """Elimina una marca por ID"""
    try:
        ObjectId(id)  # Validar ID
        
        result = marcas_collection.delete_one({"_id": ObjectId(id)})
        
        if result.deleted_count == 0:
            logger.warning(f"Marca no encontrada para eliminar: {id}")
            return None
        
        logger.info(f"Marca eliminada: {id}")
        return result
        
    except Exception as e:
        logger.error(f"Error eliminando marca {id}: {str(e)}")
        return None

# =========================
# UTILIDADES ESPECÍFICAS DE MARCAS
# =========================
def marca_existe(id: str) -> bool:
    """Verifica si existe una marca por ID"""
    try:
        return marcas_collection.count_documents({"_id": ObjectId(id)}) > 0
    except:
        return False

def marca_existe_por_nombre(nombre: str) -> bool:
    """Verifica si existe una marca por nombre"""
    try:
        return marcas_collection.count_documents({
            "nombre": {"$regex": nombre, "$options": "i"}
        }) > 0
    except:
        return False

def buscar_marcas(termino: str, limit: int = 10) -> List[Dict[str, Any]]:
    """Busca marcas por nombre"""
    try:
        marcas = list(marcas_collection.find({
            "nombre": {"$regex": termino, "$options": "i"}
        }).limit(limit))
        return [serialize_marca(m) for m in marcas]
    except Exception as e:
        logger.error(f"Error buscando marcas '{termino}': {str(e)}")
        return []

# =========================
# DEBUG Y MANTENIMIENTO
# =========================
def debug_marca(id: str) -> Dict[str, Any]:
    """Debug completo de una marca"""
    try:
        ObjectId(id)
        marca = marcas_collection.find_one({"_id": ObjectId(id)})
        
        return {
            "debug_info": {
                "id_valid": True,
                "marca_exists": marca is not None,
                "total_marcas": contar_marcas()
            },
            "marca": serialize_marca(marca),
            "raw_marca": str(marca) if marca else None
        }
    except Exception as e:
        return {
            "debug_info": {
                "id_valid": False,
                "error": str(e)
            },
            "marca": None
        }

def limpiar_coleccion_marcas() -> Dict[str, Any]:
    """⚠️ LIMPIAR COLECCIÓN (SOLO DESARROLLO)"""
    try:
        result = marcas_collection.delete_many({})
        return {
            "message": "Colección de marcas limpiada",
            "deleted_count": result.deleted_count
        }
    except Exception as e:
        logger.error(f"Error limpiando colección marcas: {str(e)}")
        return {"error": str(e)}