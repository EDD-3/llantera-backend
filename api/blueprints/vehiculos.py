from flask import Flask, escape, request, Blueprint, current_app, jsonify
from api.models import Vehiculo
from api.schemas import VehiculoSchema
from json import loads as jloads
from flask_cors import CORS
from api.utils import helpers

vehiculo = Blueprint("vehiculo", __name__)
vehiculo_schema = VehiculoSchema()
CORS(vehiculo)


@vehiculo.route("/api/vehiculos", methods=["GET"])
def get_vehicles():
    try:
        return helpers.get_rows(Vehiculo,vehiculo_schema)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@vehiculo.route("/api/vehiculo/<id>", methods=["GET"])
def get_vehicle(id):
    try:
        examiner = helpers.Examiner(
            id=id,
            model=Vehiculo,
            schema=vehiculo_schema
        )
        return helpers.get_row(examiner)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    return vehiculo_schema.dump(vehiculo), 200


@vehiculo.route("/api/vehiculo", methods=["POST"])
def create_vehicle():
    try:
        examiner = helpers.Examiner(
            model=Vehiculo,
            schema=vehiculo_schema,
            unwanted_columns=['id', 'fecha_registro'],
            json_data=jloads(request.data)
        )
        return helpers.insert_row(examiner)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@vehiculo.route("/api/vehiculo/<id>", methods=["DELETE"])
def delete_vehicle(id):
    try:
        examiner = helpers.Examiner(
            id=id,
            model=Vehiculo,
            schema=vehiculo_schema
        )
        return helpers.delete_row(examiner)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@vehiculo.route("/api/vehiculo/<id>", methods=["PUT"])
def update_vehicle(id):
    try:
        examiner = helpers.Examiner(
            id=id,
            model=Vehiculo,
            schema=vehiculo_schema,
            unwanted_columns=["id", "fecha_registro"],
            json_data=jloads(request.data)
        )
        return helpers.update_row(examiner)
    except Exception as e:
        return jsonify({"error": str(e)}), 500