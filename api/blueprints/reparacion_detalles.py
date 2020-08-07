from flask import Flask, escape, request, Blueprint, current_app, jsonify
from api.models import ReparacionDetalle
from api.schemas import ReparacionDetalleSchema
from json import loads as jloads
from flask_cors import CORS
from api.utils import helpers

reparacion_detalle = Blueprint("reparacion_detalle", __name__)
reparacion_detalle_schema = ReparacionDetalleSchema()
CORS(reparacion_detalle)


@reparacion_detalle.route("/api/reparacionDetalles", methods=["GET"])
def get_repair_details():
    try:
        return helpers.get_rows(ReparacionDetalle,reparacion_detalle_schema)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@reparacion_detalle.route("/api/reparacionDetalle/<id>", methods=["GET"])
def get_repair_detail(id):
    try:
        examiner = helpers.Examiner(
            id=id,
            model=ReparacionDetalle,
            schema=reparacion_detalle_schema
        )
        return helpers.get_row(examiner)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@reparacion_detalle.route("/api/reparacionDetalle", methods=["POST"])
def create_repair_detail():
    try:
        examiner = helpers.Examiner(
            model=ReparacionDetalle,
            schema=reparacion_detalle_schema,
            unwanted_columns=['id'],
            json_data=jloads(request.data)
        )
        return helpers.insert_row(examiner)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@reparacion_detalle.route("/api/reparacionDetalle/<id>", methods=["DELETE"])
def delete_repair_detail(id):
    try:
        examiner = helpers.Examiner(
            id=id,
            model=ReparacionDetalle,
            schema=reparacion_detalle_schema
        )
        return helpers.delete_row(examiner)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@reparacion_detalle.route("/api/reparacionDetalle/<id>", methods=["PUT"])
def update_repair_detail(id):
    try:
        examiner = helpers.Examiner(
            id=id,
            model=ReparacionDetalle,
            schema=reparacion_detalle_schema,
            unwanted_columns=["id"],
            json_data=jloads(request.data)
        )
        return helpers.update_row(examiner)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
