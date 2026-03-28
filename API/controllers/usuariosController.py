from flask import request, jsonify
from models.usuariosModel import (
    obtener_usuarios, obtener_usuario,
    insertar_usuarios, insertar_usuario,
    actualizar_usuario, eliminar_usuario
)

def get_usuarios():
    usuarios = obtener_usuarios()  # Lista de documentos desde MongoDB
    # Convertimos ObjectId a string
    for u in usuarios:
        u["_id"] = str(u["_id"])
    return jsonify(usuarios)

def get_usuario(id):
    usuario = obtener_usuario(id)
    if not usuario:
        return jsonify({"error": "Usuario no encontrado"}), 404
    return jsonify(usuario)

def crear_usuarios():
    data = request.get_json()
    resultado = insertar_usuarios(data)
    return jsonify({"inserted_ids": [str(id) for id in resultado.inserted_ids]})

def crear_usuario():
    data = request.get_json()
    resultado = insertar_usuario(data)
    return jsonify({"inserted_id": str(resultado.inserted_id)})

def actualizar_usuario_controller(id):
    data = request.get_json()
    actualizar_usuario(id, data)
    return jsonify({"message": "Usuario actualizado"})

def eliminar_usuario_controller(id):
    eliminar_usuario(id)
    return jsonify({"message": "Usuario eliminado"})