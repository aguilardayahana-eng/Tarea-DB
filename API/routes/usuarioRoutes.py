from flask import Blueprint
from controllers.usuariosController import (
    get_usuarios, get_usuario, crear_usuarios, crear_usuario,
    actualizar_usuario_controller, eliminar_usuario_controller
)

usuarios_bp = Blueprint("usuarios", __name__)

usuarios_bp.route("/", methods=["GET"])(get_usuarios)
usuarios_bp.route("/<id>", methods=["GET"])(get_usuario)
usuarios_bp.route("/multiple", methods=["POST"])(crear_usuarios)
usuarios_bp.route("/", methods=["POST"])(crear_usuario)
usuarios_bp.route("/<id>", methods=["PUT"])(actualizar_usuario_controller)
usuarios_bp.route("/<id>", methods=["DELETE"])(eliminar_usuario_controller)