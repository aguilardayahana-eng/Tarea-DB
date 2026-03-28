from config.db import conectar_db
from bson import ObjectId

db = conectar_db()
usuarios_collection = db["usuarios"]

from config.db import conectar_db

def obtener_usuarios():
    db = conectar_db()
    # find() devuelve un cursor, lo convertimos a lista
    return list(db.usuarios.find())

def obtener_usuario(id):
    return usuarios_collection.find_one({"_id": ObjectId(id)})

def insertar_usuarios(data):
    return usuarios_collection.insert_many(data)

def insertar_usuario(data):
    return usuarios_collection.insert_one(data)

def actualizar_usuario(id, data):
    return usuarios_collection.update_one({"_id": ObjectId(id)}, {"$set": data})

def eliminar_usuario(id):
    return usuarios_collection.delete_one({"_id": ObjectId(id)})