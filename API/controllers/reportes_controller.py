from flask import jsonify
from config.db import conectar_db

def marcas_con_ventas():
    """
    Retorna todas las marcas que tienen al menos una venta,
    usando directamente el campo 'marca' de la colección ventas.
    """
    db = conectar_db()
    marcas = db.ventas.distinct("marca")  # toma todas las marcas únicas de ventas
    return jsonify(marcas)

def ventas_por_fecha(fecha=None):
    """
    Retorna todas las ventas de una fecha específica.
    Si no se pasa fecha, retorna todas las ventas.
    
    fecha: string en formato 'YYYY-MM-DD', por ejemplo '2026-03-23'
    """
    db = conectar_db()
    filtro = {}
    if fecha:
        filtro["fecha"] = fecha
    
    ventas = list(db.ventas.find(filtro))
    # Convertir ObjectId a string
    for v in ventas:
        v["_id"] = str(v["_id"])
    return jsonify(ventas)