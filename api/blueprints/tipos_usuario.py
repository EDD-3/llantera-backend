from flask import Flask, escape, request, Blueprint, current_app, jsonify
from api.models import TipoUsuario
from api.schemas import TipoUsuarioSchema
from api import bcrypt, db
from json import loads as jloads
from flask_cors import CORS

tipo_usuario = Blueprint("tipo_usuario", __name__)
tipo_usuario_schema = TipoUsuarioSchema()
CORS(tipo_usuario)


@tipo_usuario.route("/api/tiposUsuario", methods=["GET"])
def get_user_types():
    try:
        lst_tipo_usuario = []
        for tipo_usuario in TipoUsuario.query.all():
            lst_tipo_usuario.append(tipo_usuario_schema.dump(tipo_usuario))
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    return jsonify(lst_tipo_usuario), 200


@tipo_usuario.route("/api/tipoUsuario/<id>", methods=["GET"])
def get_user_type(id):
    try:
        tipo_usuario = TipoUsuario.query.filter_by(id=id).first()
        if not tipo_usuario:
            return jsonify({"error": "Invalid id, user type was not found"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    return tipo_usuario_schema.dump(tipo_usuario), 200


@tipo_usuario.route("/api/tipoUsuario", methods=["POST"])
def create_user_type():
    try:
        nuevo_tipo_usuario = jloads(request.data)
        tipo_usuario = TipoUsuario(
            denominacion_usuario=nuevo_tipo_usuario["denominacion_usuario"],
            descripcion=nuevo_tipo_usuario["descripcion"],
        )

        db.session.add(tipo_usuario)
        db.session.commit()
        return jsonify({"Message": "User type successfully created"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@tipo_usuario.route("/api/tipoUsuario/<id>", methods=["DELETE"])
def delete_user_type(id):
    try:
        delete_tipo_usuario = TipoUsuario.query.filter_by(id=id).first()
        if not delete_tipo_usuario:
            return jsonify({"error": "Invalid id, user type was not found"}), 400
        db.session.delete(delete_tipo_usuario)
        db.session.commit()
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    return jsonify({"Deleted": "Success"}), 200

@tipo_usuario.route("/api/tipoUsuario/<id>", methods=["PUT"])
def update_user_type(id):
    try:
        update_values = jloads(request.data)
        if not TipoUsuario.query.filter_by(id=id).first():
            return jsonify({"error": "Invalid id, user type was not found"}), 400
        TipoUsuario.query.filter_by(id=id).update(update_values)
        db.session.commit()
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    return jsonify({"Update": "Success"}), 200