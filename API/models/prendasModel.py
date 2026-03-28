from config.db import conectar_db
from bson import ObjectId

db = conectar_db()
prendas_collection = db["prendas"]

def obtener_prendas():
    db = conectar_db()
    return list(db.prendas.find())

def obtener_prenda(id):
    return prendas_collection.find_one({"_id": ObjectId(id)})

def insertar_prendas(data):
    return prendas_collection.insert_many(data)

def insertar_prenda(data):
    return prendas_collection.insert_one(data)

def actualizar_prenda(id, data):
    return prendas_collection.update_one({"_id": ObjectId(id)}, {"$set": data})

def eliminar_prenda(id):
    return prendas_collection.delete_one({"_id": ObjectId(id)})