from flask import Blueprint, request
from controllers import reportes_controller

reportes_bp = Blueprint("reportes_bp", __name__)

# Endpoint para marcas con ventas
reportes_bp.route("/reportes/marcas-con-ventas", methods=["GET"])(reportes_controller.marcas_con_ventas)

# Endpoint para ventas por fecha
@reportes_bp.route("/reportes/ventas", methods=["GET"])
def ventas_fecha():
    fecha = request.args.get("fecha")  # ?fecha=2026-03-23
    return reportes_controller.ventas_por_fecha(fecha)