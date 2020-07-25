from flask import Flask, escape, request, Blueprint, current_app, jsonify
from api.models import Reparacion
from api.schemas import ReparacionSchema
from json import loads as jloads
from flask_cors import CORS
from api.utils import helpers

reparacion = Blueprint("reparacion", __name__)
reparacion_schema = ReparacionSchema()
CORS(reparacion)

@reparacion.route("/api/reparaciones", methods=["GET"])
def get_repairs():
    try:
        return helpers.get_rows(Reparacion,reparacion_schema)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@reparacion.route("/api/reparacion/<id>", methods=["GET"])
def get_repair(id):
    try:
        examiner = helpers.Examiner(
            id=id,
            model=Reparacion,
            schema=reparacion_schema
        )
        return helpers.get_row(examiner)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@reparacion.route("/api/reparacion", methods=["POST"])
def create_repair():
    try:
        examiner = helpers.Examiner(
            model=Reparacion,
            schema=reparacion_schema,
            unwanted_columns=['id', 'fecha_realizacion'],
            json_data=jloads(request.data)
        )
        return helpers.insert_row(examiner)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@reparacion.route("/api/reparacion/<id>", methods=["DELETE"])
def delete_repair(id):
    try:
        examiner = helpers.Examiner(
            id=id,
            model=Reparacion,
            schema=reparacion_schema
        )
        return helpers.delete_row(examiner)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@reparacion.route("/api/reparacion/<id>", methods=["PUT"])
def update_repair(id):
    try:
        examiner = helpers.Examiner(
            id=id,
            model=Reparacion,
            schema=reparacion_schema,
            unwanted_columns=["id", 'fecha_realizacion'],
            json_data=jloads(request.data)
        )
        return helpers.update_row(examiner)
    except Exception as e:
        return jsonify({"error": str(e)}), 500