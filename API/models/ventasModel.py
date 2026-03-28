from config.db import conectar_db
from bson import ObjectId

# Conectar a la colección ventas
db = conectar_db()
ventas_collection = db["ventas"]

def obtener_ventas():
    """Devuelve todas las ventas"""
    ventas = list(ventas_collection.find())
    # Convertir ObjectId a string
    for venta in ventas:
        venta["_id"] = str(venta["_id"])
    return ventas

def insertar_ventas(data):
    """Inserta varias ventas (lista de dicts)"""
    if isinstance(data, list):
        resultado = ventas_collection.insert_many(data)
        return [str(_id) for _id in resultado.inserted_ids]
    else:
        raise ValueError("Data debe ser una lista de diccionarios")

def insertar_venta(data):
    """Inserta una sola venta"""
    resultado = ventas_collection.insert_one(data)
    data["_id"] = str(resultado.inserted_id)
    return data

def actualizar_venta(id, data):
    """Actualiza una venta por id"""
    resultado = ventas_collection.update_one(
        {"_id": ObjectId(id)},
        {"$set": data}
    )
    return resultado.matched_count  # retorna 0 si no se encontró

def eliminar_venta(id):
    """Elimina una venta por id"""
    resultado = ventas_collection.delete_one({"_id": ObjectId(id)})
    return resultado.deleted_count  # retorna 0 si no se encontró