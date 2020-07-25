from flask import Flask, escape, request, Blueprint, current_app, jsonify
from api.models import Vehiculo
from api.schemas import VehiculoSchema
from api import db
from datetime import date
from json import loads as jloads
from flask_cors import CORS

vehiculo = Blueprint("vehiculo", __name__)
vehiculo_schema = VehiculoSchema()


@vehiculo.route("/api/vehiculos", methods=["GET"])
def get_vehicles():
    try:
        vehiculos = []
        for vehiculo in Vehiculo.query.all():
            lst_vehiculo.append(vehiculo_schema.dump(vehiculo))
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    return jsonify(lst_vehiculo), 200


@vehiculo.route("/api/vehiculo/<id>", methods=["GET"])
def get_vehicle(id):
    try:
        vehiculo = Vehiculo.query.filter_by(id=id).first()
        if not vehiculo:
            return jsonify({"error": "Invalid id, customer was not found"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    return vehiculo_schema.dump(vehiculo), 200


@vehiculo.route("/api/vehiculo", methods=["POST"])
def create_vehicle():
    try:
        nuevo_vehiculo = json.loads(request.data)
        vehiculo = Vehiculo(
            modelo=nuevo_vehiculo["modelo"],
            descripcion=nuevo_vehiculo["descripcion"],
            cliente_id=nuevo_vehiculo["cliente_id"],
            fecha_fabricacion=date.fromisoformat(nuevo_vehiculo["fecha_fabricacion"]),
        )

        db.session.add(vehiculo)
        db.session.commit()
        return jsonify({"Message": "Vehicle successfully created"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500