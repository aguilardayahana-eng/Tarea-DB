from flask import request, jsonify
from models.marcasModel import (
    obtener_marcas, obtener_marca,
    insertar_marcas, insertar_marca,
    actualizar_marca, eliminar_marca
)

def get_marcas():
    marcas = obtener_marcas()
    for m in marcas:
        m["_id"] = str(m["_id"])
    return jsonify(marcas)

def get_marca(id):
    marca = obtener_marca(id)
    if not marca:
        return jsonify({"error": "Marca no encontrada"}), 404
    return jsonify(marca)

def crear_marcas():
    data = request.get_json()
    resultado = insertar_marcas(data)
    return jsonify({"inserted_ids": [str(id) for id in resultado.inserted_ids]})

def crear_marca():
    data = request.get_json()
    resultado = insertar_marca(data)
    return jsonify({"inserted_id": str(resultado.inserted_id)})

def actualizar_marca_controller(id):
    data = request.get_json()
    actualizar_marca(id, data)
    return jsonify({"message": "Marca actualizada"})

def eliminar_marca_controller(id):
    eliminar_marca(id)
    return jsonify({"message": "Marca eliminada"})