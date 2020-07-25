from flask import Flask, escape, request, Blueprint, current_app, jsonify
from api.models import TipoParte
from api.schemas import TipoParteSchema
from json import loads as jloads
from flask_cors import CORS
from api.utils import helpers

tipo_parte = Blueprint("tipo_parte", __name__)
tipo_parte_schema = TipoParteSchema()
CORS(tipo_parte)

@tipo_parte.route("/api/tiposParte", methods=["GET"])
def get_part_types():
    try:
        return helpers.get_rows(TipoParte,tipo_parte_schema)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@tipo_parte.route("/api/tipoParte/<id>", methods=["GET"])
def get_part_type(id):
    try:
        examiner = helpers.Examiner(
            id=id,
            model=TipoParte,
            schema=tipo_parte_schema
        )
        return helpers.get_row(examiner)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@tipo_parte.route("/api/tipoParte", methods=["POST"])
def create_part_type():
    try:
        examiner = helpers.Examiner(
            model=TipoParte,
            schema=tipo_parte_schema,
            unwanted_columns=['id'],
            json_data=jloads(request.data)
        )
        return helpers.insert_row(examiner)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@tipo_parte.route("/api/tipoParte/<id>", methods=["DELETE"])
def delete_part_type(id):
    try:
        examiner = helpers.Examiner(
            id=id,
            model=TipoParte,
            schema=tipo_parte_schema
        )
        return helpers.delete_row(examiner)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@tipo_parte.route("/api/tipoParte/<id>", methods=["PUT"])
def update_part_type(id):
    try:
        examiner = helpers.Examiner(
            id=id,
            model=TipoParte,
            schema=tipo_parte_schema,
            unwanted_columns=["id"],
            json_data=jloads(request.data)
        )
        return helpers.update_row(examiner)
    except Exception as e:
        return jsonify({"error": str(e)}), 500