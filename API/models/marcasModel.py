from config.db import conectar_db
from bson import ObjectId

db = conectar_db()
marcas_collection = db["marcas"]

def obtener_marcas():
    db = conectar_db()
    return list(db.marcas.find())

def obtener_marca(id):
    return marcas_collection.find_one({"_id": ObjectId(id)})

def insertar_marcas(data):
    return marcas_collection.insert_many(data)

def insertar_marca(data):
    return marcas_collection.insert_one(data)

def actualizar_marca(id, data):
    return marcas_collection.update_one({"_id": ObjectId(id)}, {"$set": data})

def eliminar_marca(id):
    return marcas_collection.delete_one({"_id": ObjectId(id)})