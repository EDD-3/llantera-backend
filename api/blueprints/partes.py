from flask import Flask, escape, request, Blueprint, current_app, jsonify
from api.models import Parte
from api.schemas import ParteSchema
from json import loads as jloads
from flask_cors import CORS
from api.utils import helpers

parte = Blueprint("parte", __name__)
parte_schema = ParteSchema()
CORS(parte)

@parte.route("/api/partes", methods=["GET"])
def get_parts():
    try:
        return helpers.get_rows(Parte,parte_schema)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@parte.route("/api/parte/<id>", methods=["GET"])
def get_part(id):
    try:
        examiner = helpers.Examiner(
            id=id,
            model=Parte,
            schema=parte_schema
        )
        return helpers.get_row(examiner)

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@parte.route("/api/parte", methods=["POST"])
def create_part():
    try:
        examiner = helpers.Examiner(
            model=Parte,
            schema=parte_schema,
            unwanted_columns=['id'],
            json_data=jloads(request.data)
        )
        return helpers.insert_row(examiner)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@parte.route("/api/parte/<id>", methods=["DELETE"])
def delete_part(id):
    try:
        examiner = helpers.Examiner(
            id=id,
            model=Parte,
            schema=parte_schema
        )
        return helpers.delete_row(examiner)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@parte.route("/api/parte/<id>", methods=["PUT"])
def update_part(id):
    try:
        examiner = helpers.Examiner(
            id=id,
            model=Parte,
            schema=parte_schema,
            unwanted_columns=["id"],
            json_data=jloads(request.data)
        )
        return helpers.update_row(examiner)
    except Exception as e:
        return jsonify({"error": str(e)}), 500