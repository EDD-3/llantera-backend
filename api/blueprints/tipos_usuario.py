from flask import Flask, escape, request, Blueprint, current_app, jsonify
from api.models import TipoUsuario
from api.schemas import TipoUsuarioSchema
from json import loads as jloads
from flask_cors import CORS
from api.utils import helpers

tipo_usuario = Blueprint("tipo_usuario", __name__)
tipo_usuario_schema = TipoUsuarioSchema()
CORS(tipo_usuario)


@tipo_usuario.route("/api/tiposUsuario", methods=["GET"])
def get_user_types():
    try:
        return helpers.get_rows(TipoUsuario, tipo_usuario_schema)

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@tipo_usuario.route("/api/tipoUsuario/<id>", methods=["GET"])
def get_user_type(id):
    try:
        examiner = helpers.Examiner(id=id,model=TipoUsuario,schema=tipo_usuario_schema)
        return helpers.get_row(examiner)

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@tipo_usuario.route("/api/tipoUsuario", methods=["POST"])
def create_user_type():
    try:
        examiner = helpers.Examiner(
            id=id,
            model=TipoUsuario,
            schema=tipo_usuario_schema,
            unwanted_columns=['id'],
            json_data=jloads(request.data)

        )

        return helpers.insert_row(examiner)

    except Exception as e:
        return jsonify({"error": str(e)}), 500



@tipo_usuario.route("/api/tipoUsuario/<id>", methods=["DELETE"])
def delete_user_type(id):
    try:
        examiner = helpers.Examiner(
            id=id,
            model=TipoUsuario,
            schema=tipo_usuario_schema,
        )
        return helpers.delete_row(examiner)

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@tipo_usuario.route("/api/tipoUsuario/<id>", methods=["PUT"])
def update_user_type(id):
    try:
        examiner = helpers.Examiner(
            id=id,
            model=TipoUsuario,
            schema=tipo_usuario_schema,
            json_data=jloads(request.data),
            unwanted_columns=["id"],
        )
        return helpers.update_row(examiner)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

