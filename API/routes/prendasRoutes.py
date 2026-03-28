from flask import Blueprint
from controllers.prendasController import (
    get_prendas, get_prenda, crear_prendas, crear_prenda,
    actualizar_prenda_controller, eliminar_prenda_controller
)

prendas_bp = Blueprint("prendas", __name__)

prendas_bp.route("/", methods=["GET"])(get_prendas)
prendas_bp.route("/<id>", methods=["GET"])(get_prenda)
prendas_bp.route("/multiple", methods=["POST"])(crear_prendas)
prendas_bp.route("/", methods=["POST"])(crear_prenda)
prendas_bp.route("/<id>", methods=["PUT"])(actualizar_prenda_controller)
prendas_bp.route("/<id>", methods=["DELETE"])(eliminar_prenda_controller)