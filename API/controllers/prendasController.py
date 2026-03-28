from flask import request, jsonify
from models.prendasModel import (
    obtener_prendas, obtener_prenda,
    insertar_prendas, insertar_prenda,
    actualizar_prenda, eliminar_prenda
)

def get_prendas():
    prendas = obtener_prendas()
    for p in prendas:
        p["_id"] = str(p["_id"])
    return jsonify(prendas)

def get_prenda(id):
    prenda = obtener_prenda(id)
    if not prenda:
        return jsonify({"error": "Prenda no encontrada"}), 404
    return jsonify(prenda)

def crear_prendas():
    data = request.get_json()
    resultado = insertar_prendas(data)
    return jsonify({"inserted_ids": [str(id) for id in resultado.inserted_ids]})

def crear_prenda():
    data = request.get_json()
    resultado = insertar_prenda(data)
    return jsonify({"inserted_id": str(resultado.inserted_id)})

def actualizar_prenda_controller(id):
    data = request.get_json()
    actualizar_prenda(id, data)
    return jsonify({"message": "Prenda actualizada"})

def eliminar_prenda_controller(id):
    eliminar_prenda(id)
    return jsonify({"message": "Prenda eliminada"})