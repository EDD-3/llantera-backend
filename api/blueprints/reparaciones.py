from flask import Flask, escape, request, Blueprint, current_app, jsonify
import json
from api.models import Reparacion
from api.schemas import ReparacionSchema
from api import bcrypt, db

reparacion = Blueprint("reparacion", __name__)
reparacion_schema = ReparacionSchema()


@reparacion.route("/api/reparaciones", methods=["GET"])
def get_repairs():
    try:
        lst_reparacion = []
        for reparacion in Reparacion.query.all():
            lst_reparacion.append(reparacion_schema.dump(reparacion))
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    return jsonify(lst_reparacion), 200


@reparacion.route("/api/reparacion/<id>", methods=["GET"])
def get_repair(id):
    try:
        reparacion = Reparacion.query.filter_by(id=id).first()
        if not reparacion:
            return jsonify({"error": "Invalid id, record not found"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    return reparacion_schema.dump(reparacion), 200


@reparacion.route("/api/reparacion", methods=["POST"])
def create_repair():
    try:
        nuevo_reparacion = json.loads(request.data)
        reparacion = Reparacion(
            usuario_id=nuevo_reparacion["usuario_id"],
            cliente_id=nuevo_reparacion["cliente_id"],
            garantia_id=nuevo_reparacion["garantia_id"],
            total=nuevo_reparacion["total"],
        )

        db.session.add(reparacion)
        db.session.commit()
        return jsonify({"Message": "Reparacion successfully created"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500