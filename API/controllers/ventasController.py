from flask import request, jsonify
from config.db import conectar_db
from bson import ObjectId

# Conectar a la DB y a la colección ventas
db = conectar_db()
ventas_collection = db["ventas"]  # nombre de tu colección

# GET /ventas
def get_ventas():
    ventas = list(ventas_collection.find())
    # Convertir ObjectId a string
    for venta in ventas:
        venta["_id"] = str(venta["_id"])
    return jsonify(ventas)

# POST /ventas
def crear_venta():
    data = request.get_json()
    resultado = ventas_collection.insert_one(data)
    data["_id"] = str(resultado.inserted_id)
    return jsonify(data)

# PUT /ventas/<id>
def actualizar_venta(id):
    data = request.get_json()
    resultado = ventas_collection.update_one(
        {"_id": ObjectId(id)},
        {"$set": data}
    )
    if resultado.matched_count == 0:
        return jsonify({"error": "Venta no encontrada"}), 404
    return jsonify({"message": "Venta actualizada"})

# DELETE /ventas/<id>
def eliminar_venta(id):
    resultado = ventas_collection.delete_one({"_id": ObjectId(id)})
    if resultado.deleted_count == 0:
        return jsonify({"error": "Venta no encontrada"}), 404
    return jsonify({"message": "Venta eliminada"})