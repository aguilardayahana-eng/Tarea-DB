from flask import Blueprint
from controllers.marcasController import (
    get_marcas, get_marca, crear_marcas, crear_marca,
    actualizar_marca_controller, eliminar_marca_controller
)

marcas_bp = Blueprint("marcas", __name__)

marcas_bp.route("/", methods=["GET"])(get_marcas)
marcas_bp.route("/<id>", methods=["GET"])(get_marca)
marcas_bp.route("/multiple", methods=["POST"])(crear_marcas)
marcas_bp.route("/", methods=["POST"])(crear_marca)
marcas_bp.route("/<id>", methods=["PUT"])(actualizar_marca_controller)
marcas_bp.route("/<id>", methods=["DELETE"])(eliminar_marca_controller)