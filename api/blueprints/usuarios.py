from flask import Flask, escape, request, Blueprint, current_app, jsonify
from api.models import Usuario
from api.schemas import UsuarioSchema
from api import bcrypt, db
from json import loads as jloads

usuario = Blueprint("usuario", __name__)
usuario_schema = UsuarioSchema()


@usuario.route("/api/usuarios", methods=["GET"])
def get_users():
    try:
        usuarios = []

        for usuario in Usuario.query.all():
            usuarios.append(usuario_schema.dump(usuario))

        if len(usuarios) == 0:
            return jsonify({"error": "No users in database"}), 404

    except Exception as e:
        return jsonify({"error": str(e)}), 500

    return jsonify(usuarios), 200



@usuario.route("/api/usuario/<id>", methods=["GET"])
def get_user(id):
    try:
        usuario = Usuario.query.filter_by(id=id).first()

        if usuario is not None:
            return usuario_schema.dump(usuario), 200

        else:
            return jsonify({"error": "Invalid id, user was not found"}), 404

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@usuario.route("/api/usuario/login", methods=["GET"])
def verify_login():
    try:
        login_credentials = jloads(request.data)
        usuario = Usuario.query.filter_by(
            nombre_usuario=login_credentials["nombre_usuario"]
        ).first()

        if (usuario is not None) and bcrypt.check_password_hash(
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
        nuevo_usuario = jloads(request.data)
        table_columns = [
            column.name for column in Usuario.__table__.columns if column.name != "id"
        ]

        for field in nuevo_usuario:
            if field in table_columns:
                table_columns.remove(field)

        if len(table_columns) == 0:
            usuario = Usuario(
                nombre_usuario=nuevo_usuario["nombre_usuario"],
                contrasena=bcrypt.generate_password_hash(nuevo_usuario["contrasena"]),
                empleado_id=nuevo_usuario["empleado_id"],
                tipo_usuario_id=nuevo_usuario["tipo_usuario_id"],
            )
            db.session.add(usuario)
            db.session.commit()
            nuevo_usuario = Usuario.query.order_by(Usuario.id.desc()).first()

        else:
            return jsonify({"missing fields":table_columns}), 400

    except Exception as e:
        return jsonify({"error": str(e)}), 500

    return usuario_schema.dump(nuevo_usuario), 200


@usuario.route("/api/usuario/<id>", methods=["DELETE"])
def delete_user(id):
    try:
        usuario = Usuario.query.filter_by(id=id).first()

        if usuario is not None:
            db.session.delete(usuario)
            db.session.commit()

        else:
            return jsonify({"error": "Invalid id, user was not found"}), 404

    except Exception as e:
        return jsonify({"error": str(e)}), 500

    return jsonify({"message": "Success"}), 200


@usuario.route("/api/usuario/<id>", methods=["PUT"])
def update_user(id):
    try:
        update_dict = jloads(request.data)
        table_columns = [
            column.name for column in Usuario.__table__.columns if column.name != "id"
        ]
        usuario = Usuario.query.filter_by(id=id).first()

        for field in update_dict:

            if field in table_columns:
                table_columns.remove(field)
        
        if usuario is not None:
            if len(table_columns) == 0:
                update_dict["contrasena"] = bcrypt.generate_password_hash(
                    update_dict["contrasena"]
            )
                Usuario.query.filter_by(id=id).update(update_dict)
                db.session.commit()

            else:
                return jsonify({"missing fields": table_columns}),400

        else:
            return jsonify({"error": "Invalid id, user not found"}), 404
            
    except Exception as e:
        return jsonify({"error": str(e)}), 500

    return ({"message": "Success"}), 200
