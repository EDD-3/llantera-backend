from flask import Flask, escape, request, Blueprint, current_app, jsonify
import json
from api.models import Usuario
from api.schemas import UsuarioSchema
from api import bcrypt, db

usuario = Blueprint("usuario", __name__)
usuario_schema = UsuarioSchema()


@usuario.route("/api/usuarios", methods=["GET"])
def get_users():
    try:
        lst_usuario = []
        for usuario in Usuario.query.all():
            lst_usuario.append(usuario_schema.dump(usuario))
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    return jsonify(lst_usuario), 200


@usuario.route("/api/usuario/<id>", methods=["GET"])
def get_user(id):
    try:
        usuario = Usuario.query.filter_by(id=id).first()
        if not usuario:
            return jsonify({"error": "Invalid id, user was not found"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    return usuario_schema.dump(usuario), 200


@usuario.route("/api/usuario/login", methods=["GET"])
def verify_login():
    try:
        login_credentials = json.loads(request.data)
        usuario = Usuario.query.filter_by(
            nombre_usuario=login_credentials["nombre_usuario"]
        ).first()
        if usuario and bcrypt.check_password_hash(
            usuario.contrasena, login_credentials["contrasena"]
        ):
            return jsonify({"validCredentials": True}), 200
        else:
            return jsonify({"validCredentials": False}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@usuario.route("/api/usuario", methods=["POST"])
def create_user():
    try:
        nuevo_usuario = json.loads(request.data)
        usuario = Usuario(
        nombre_usuario=nuevo_usuario["nombre_usuario"],
        contrasena=bcrypt.generate_password_hash(nuevo_usuario["contrasena"]),
        empleado_id=nuevo_usuario["empleado_id"],
        tipo_usuario_id=nuevo_usuario["tipo_usuario_id"],
    )
        db.session.add(usuario)
        db.session.commit()
        return jsonify({"Message": "User successfully created"}),200
    except Exception as e:
        return jsonify({"error": str(e)}), 500