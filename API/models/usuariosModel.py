"""
Modelo de Usuarios para MongoDB
Manejo completo de operaciones CRUD con validaciones y serialización
"""
from config.db import conectar_db
from bson import ObjectId
from typing import List, Dict, Any, Optional, Union
import logging
from datetime import datetime

# Configuración
logger = logging.getLogger(__name__)
db = conectar_db()
usuarios_collection = db["usuarios"]

def serialize_usuario(usuario: Optional[Dict[str, Any]]) -> Optional[Dict[str, Any]]:
    """Serializa un usuario convirtiendo ObjectId a string"""
    if not usuario:
        return None
    
    serialized = usuario.copy()
    if '_id' in serialized:
        serialized['_id'] = str(serialized['_id'])
    
    # Serializar otros ObjectId si existen
    for key, value in serialized.items():
        if isinstance(value, ObjectId):
            serialized[key] = str(value)
    
    return serialized

def deserialize_id(data: Dict[str, Any]) -> Dict[str, Any]:
    """Elimina _id del data para evitar conflictos en inserts/updates"""
    data_copy = data.copy()
    data_copy.pop('_id', None)
    return data_copy

# =========================
# READ OPERATIONS
# =========================
def obtener_usuarios(limit: int = 100, skip: int = 0) -> List[Dict[str, Any]]:
    """Obtiene lista de usuarios con paginación"""
    try:
        pipeline = [
            {"$skip": skip},
            {"$limit": limit}
        ]
        cursor = usuarios_collection.aggregate(pipeline)
        usuarios = list(cursor)
        return [serialize_usuario(u) for u in usuarios]
    except Exception as e:
        logger.error(f"Error obteniendo usuarios: {str(e)}")
        return []

def obtener_usuario(id: str) -> Optional[Dict[str, Any]]:
    """Obtiene un usuario por ID"""
    try:
        user = usuarios_collection.find_one({"_id": ObjectId(id)})
        return serialize_usuario(user)
    except Exception as e:
        logger.warning(f"ID inválido o error obteniendo usuario {id}: {str(e)}")
        return None

def obtener_usuario_por_email(email: str) -> Optional[Dict[str, Any]]:
    """Obtiene usuario por email (útil para login)"""
    try:
        user = usuarios_collection.find_one({"email": email.lower().strip()})
        return serialize_usuario(user)
    except Exception as e:
        logger.error(f"Error buscando usuario por email {email}: {str(e)}")
        return None

# =========================
# CREATE OPERATIONS
# =========================
def insertar_usuarios(data: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Inserta múltiples usuarios"""
    try:
        # Validar que sea lista no vacía
        if not data or not isinstance(data, list):
            raise ValueError("Data debe ser una lista no vacía")
        
        # Normalizar datos
        normalized_data = []
        for item in data:
            normalized = deserialize_id(item)
            # Agregar timestamp si no existe
            if 'created_at' not in normalized:
                normalized['created_at'] = datetime.utcnow()
            normalized_data.append(normalized)
        
        result = usuarios_collection.insert_many(normalized_data)
        logger.info(f"Insertados {len(result.inserted_ids)} usuarios")
        return result
    except Exception as e:
        logger.error(f"Error insertando usuarios múltiples: {str(e)}")
        raise

def insertar_usuario(data: Dict[str, Any]) -> Dict[str, Any]:
    """Inserta un solo usuario"""
    try:
        if not isinstance(data, dict):
            raise ValueError("Data debe ser un diccionario")
        
        # Normalizar datos
        normalized = deserialize_id(data)
        if 'created_at' not in normalized:
            normalized['created_at'] = datetime.utcnow()
        if 'updated_at' not in normalized:
            normalized['updated_at'] = datetime.utcnow()
        
        result = usuarios_collection.insert_one(normalized)
        logger.info(f"Usuario insertado con ID: {str(result.inserted_id)}")
        return result
    except Exception as e:
        logger.error(f"Error insertando usuario: {str(e)}")
        raise

# =========================
# UPDATE OPERATIONS
# =========================
def actualizar_usuario(id: str, data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """Actualiza un usuario por ID"""
    try:
        # Validar ID
        ObjectId(id)
        
        # Preparar datos de actualización
        update_data = deserialize_id(data)
        update_data['updated_at'] = datetime.utcnow()
        
        result = usuarios_collection.update_one(
            {"_id": ObjectId(id)},
            {"$set": update_data}
        )
        
        if result.matched_count == 0:
            logger.warning(f"Usuario no encontrado para actualizar: {id}")
            return None
        
        logger.info(f"Usuario actualizado: {id}, modificado: {result.modified_count}")
        return result
        
    except Exception as e:
        logger.error(f"Error actualizando usuario {id}: {str(e)}")
        return None

def actualizar_usuario_por_email(email: str, data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """Actualiza usuario por email"""
    try:
        update_data = deserialize_id(data)
        update_data['updated_at'] = datetime.utcnow()
        
        result = usuarios_collection.update_one(
            {"email": email.lower().strip()},
            {"$set": update_data}
        )
        
        return result if result.matched_count > 0 else None
    except Exception as e:
        logger.error(f"Error actualizando usuario por email {email}: {str(e)}")
        return None

# =========================
# DELETE OPERATIONS
# =========================
def eliminar_usuario(id: str) -> Optional[Dict[str, Any]]:
    """Elimina un usuario por ID"""
    try:
        ObjectId(id)  # Validar ID
        
        result = usuarios_collection.delete_one({"_id": ObjectId(id)})
        
        if result.deleted_count == 0:
            logger.warning(f"Usuario no encontrado para eliminar: {id}")
            return None
        
        logger.info(f"Usuario eliminado: {id}")
        return result
        
    except Exception as e:
        logger.error(f"Error eliminando usuario {id}: {str(e)}")
        return None

def eliminar_usuario_por_email(email: str) -> Optional[Dict[str, Any]]:
    """Elimina usuario por email"""
    try:
        result = usuarios_collection.delete_one({"email": email.lower().strip()})
        return result if result.deleted_count > 0 else None
    except Exception as e:
        logger.error(f"Error eliminando usuario por email {email}: {str(e)}")
        return None

# =========================
# UTILITY & DEBUG
# =========================
def contar_usuarios() -> int:
    """Cuenta total de usuarios"""
    try:
        return usuarios_collection.count_documents({})
    except Exception as e:
        logger.error(f"Error contando usuarios: {str(e)}")
        return 0

def usuario_existe(id: str) -> bool:
    """Verifica si existe un usuario por ID"""
    try:
        return usuarios_collection.count_documents({"_id": ObjectId(id)}) > 0
    except:
        return False

def debug_usuario(id: str) -> Dict[str, Any]:
    """Debug completo de un usuario"""
    try:
        ObjectId(id)
        
        # Información básica
        user = usuarios_collection.find_one({"_id": ObjectId(id)})
        exists = user is not None
        
        # Stats de la colección
        total_usuarios = contar_usuarios()
        
        return {
            "debug_info": {
                "id_valid": True,
                "user_exists": exists,
                "total_users_in_collection": total_usuarios
            },
            "user": serialize_usuario(user),
            "raw_user": str(user) if user else None,
            "collection_stats": {
                "name": str(usuarios_collection.full_name),
                "count": total_usuarios
            }
        }
    except Exception as e:
        return {
            "debug_info": {
                "id_valid": False,
                "error": str(e)
            },
            "user": None
        }

def limpiar_coleccion() -> Dict[str, Any]:
    """⚠️ LIMPIAR COLECCIÓN (SOLO PARA DESARROLLO)"""
    try:
        result = usuarios_collection.delete_many({})
        return {
            "message": "Colección limpiada",
            "deleted_count": result.deleted_count
        }
    except Exception as e:
        logger.error(f"Error limpiando colección: {str(e)}")
        return {"error": str(e)}