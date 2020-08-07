from flask import Flask, escape, request, Blueprint, current_app, jsonify
from json import loads as jloads
from api.models import Garantia
from api.schemas import GarantiaSchema
from flask_cors import CORS
from api.utils import helpers
import uuid

garantia = Blueprint("garantia", __name__)
garantia_schema = GarantiaSchema()
CORS(garantia)


@garantia.route("/api/garantias", methods=["GET"])
def get_warranties():
    try:
        return helpers.get_rows(Garantia,garantia_schema)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@garantia.route("/api/garantia/<id>", methods=["GET"])
def get_warranty(id):
    try:
        examiner = helpers.Examiner(
            id=id,
            model=Garantia,
            schema=garantia_schema,
        )
        return helpers.get_row(examiner)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@garantia.route("/api/garantia", methods=["POST"])
def create_warranty():
    try:
        json_data=jloads(request.data)
        json_data['codigo'] = uuid.uuid4().hex
        examiner = helpers.Examiner(
            model=Garantia,
            schema=garantia_schema,
            unwanted_columns=['id','fecha_vencimiento', 'fecha_inicio'],
            json_data=json_data
        )
        return helpers.insert_row(examiner)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@garantia.route("/api/garantia/<id>", methods=["DELETE"])
def delete_warranty(id):
    try:
        examiner = helpers.Examiner(
            id=id,
            model=Garantia,
            schema=garantia_schema
        )
        return helpers.delete_row(examiner)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@garantia.route("/api/garantia/<id>", methods=["PUT"])
def update_warranty(id):
    try:
        json_data=jloads(request.data)
        json_data['codigo'] = uuid.uuid4().hex
        examiner = helpers.Examiner(
            id=id,
            model=Garantia,
            schema=garantia_schema,
            unwanted_columns=["id",'fecha_vencimiento', 'fecha_inicio'],
            json_data=jloads
        )
        return helpers.update_row(examiner)

    except Exception as e:
        return jsonify({"error": str(e)}), 500