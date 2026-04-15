from flask import Blueprint
from controllers.ventasController import (
    get_ventas,
    crear_venta,
    actualizar_venta,
    eliminar_venta
)

ventas_bp = Blueprint("ventas", __name__)

# Directamente las funciones (si tus controllers devuelven Response)
ventas_bp.route("/", methods=["GET"])(get_ventas)
ventas_bp.route("/multiple", methods=["POST"])(crear_venta)
ventas_bp.route("/<id>", methods=["PUT"])(actualizar_venta)
ventas_bp.route("/<id>", methods=["DELETE"])(eliminar_venta)