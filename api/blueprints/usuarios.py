from flask import Flask, escape, request, Blueprint, current_app, jsonify
from api.models import Usuario
from api.schemas import UsuarioSchema
from api import bcrypt, db
from json import loads as jloads
from flask_cors import CORS
from api import bcrypt
from api.utils import helpers

usuario = Blueprint("usuario", __name__)
usuario_schema = UsuarioSchema()
CORS(usuario)

@usuario.route("/api/usuarios", methods=["GET"])
def get_users():
    try:
        return helpers.get_rows(Usuario, usuario_schema)
    except Exception as e:
        return jsonify({"error": str(e)}), 500




@usuario.route("/api/usuario/<id>", methods=["GET"])
def get_user(id):
    try:
        examiner = helpers.Examiner(
            id=id,
            model=Usuario,
            schema=usuario_schema
        )
        return helpers.get_row(examiner)

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# @usuario.route("/api/usuario/login", methods=["GET"])
# def verify_login():
#     try:
#         login_credentials = jloads(request.data)
#         usuario = Usuario.query.filter_by(
#             nombre_usuario=login_credentials["nombre_usuario"]
#         ).first()

#         if (usuario is not None) and bcrypt.check_password_hash(
#             usuario.contrasena, login_credentials["contrasena"]
#         ):
#             return jsonify({"validCredentials": True}), 200

#         else:
#             return jsonify({"validCredentials": False}), 400

#     except Exception as e:
#         return jsonify({"error": str(e)}), 500


@usuario.route("/api/usuario", methods=["POST"])
def create_user():
    try:
        nuevo_usuario = jloads(request.data)
        nuevo_usuario["contrasena"] = bcrypt.generate_password_hash(nuevo_usuario["contrasena"])
        examiner = helpers.Examiner(
            model=Usuario,
            schema=usuario_schema,
            unwanted_columns=['id'],
            json_data=nuevo_usuario)

        return helpers.insert_row(examiner)

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@usuario.route("/api/usuario/<id>", methods=["DELETE"])
def delete_user(id):
    try:
        examiner = helpers.Examiner(
            id=id,
            model=Usuario,
            schema=usuario_schema
        )
        return helpers.delete_row(examiner)

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@usuario.route("/api/usuario/<id>", methods=["PUT"])
def update_user(id):
    try:
        nuevo_usuario = jloads(request.data)
        nuevo_usuario["contrasena"] = bcrypt.generate_password_hash(nuevo_usuario["contrasena"])
        examiner = helpers.Examiner(
            id=id,
            model=Usuario,
            schema=usuario_schema,
            unwanted_columns=['id'],
            json_data=nuevo_usuario
            )
        return helpers.update_row(examiner)      
    except Exception as e:
        return jsonify({"error": str(e)}), 500
