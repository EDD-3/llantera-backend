from flask import Flask, escape, request, Blueprint, current_app, jsonify
from api.models import TipoUsuario
from api.schemas import TipoUsuarioSchema
from api import bcrypt, db
from json import loads as jloads

tipo_usuario = Blueprint("tipo_usuario", __name__)
tipo_usuario_schema = TipoUsuarioSchema()


@tipo_usuario.route("/api/tiposUsuario", methods=["GET"])
def get_stocks():
    try:
        lst_tipo_usuario = []
        for tipo_usuario in TipoUsuario.query.all():
            lst_tipo_usuario.append(tipo_usuario_schema.dump(tipo_usuario))
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    return jsonify(lst_tipo_usuario), 200


@tipo_usuario.route("/api/tipoUsuario/<id>", methods=["GET"])
def get_stock(id):
    try:
        tipo_usuario = TipoUsuario.query.filter_by(id=id).first()
        if not tipo_usuario:
            return jsonify({"error": "Invalid id, stock was not found"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    return tipo_usuario_schema.dump(tipo_usuario), 200


@tipo_usuario.route("/api/tipoUsuario", methods=["POST"])
def create_stock():
    try:
        nuevo_tipo_usuario = jloads(request.data)
        tipo_usuario = TipoUsuario(
            denominacion_usuario=nuevo_tipo_usuario["denominacion_usuario"],
            descripcion=nuevo_tipo_usuario["descripcion"],
        )

        db.session.add(tipo_usuario)
        db.session.commit()
        return jsonify({"Message": "Customer successfully created"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500