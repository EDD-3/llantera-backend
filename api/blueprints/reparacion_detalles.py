from flask import Flask, escape, request, Blueprint, current_app, jsonify
from api.models import ReparacionDetalle
from api.schemas import ReparacionDetalleSchema
from api import bcrypt, db, app
from json import loads as jloads

reparacion_detalle = Blueprint("reparacion_detalle", __name__)
reparacion_detalle_schema = ReparacionDetalleSchema()


@reparacion_detalle.route("/api/reparacionDetalles", methods=["GET"])
def get_repair_details():
    try:
        lst_reparacion_detalle = []
        for reparacion_detalle in ReparacionDetalle.query.all():
            lst_reparacion_detalle.append(
                reparacion_detalle_schema.dump(reparacion_detalle)
            )
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    return jsonify(lst_reparacion_detalle), 200


@reparacion_detalle.route("/api/reparacionDetalle/<id>", methods=["GET"])
def get_repair(id):
    try:
        reparacion_detalle = ReparacionDetalle.query.filter_by(id=id).first()
        if not reparacion_detalle:
            return jsonify({"error": "Invalid id, repair details was not found"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    return reparacion_detalle_schema.dump(reparacion_detalle), 200


@reparacion_detalle.route("/api/reparacionDetalle", methods=["POST"])
def create_repair():
    try:
        nuevo_reparacion_detalle = jloads(request.data)

        for reparacion_detalle in nuevo_reparacion_detalle:
            reparacion_detalle = ReparacionDetalle(
                parte_id=reparacion_detalle["parte_id"],
                reparacion_id=reparacion_detalle["reparacion_id"],
                cantidad=reparacion_detalle["cantidad"],
            )
            db.session.add(reparacion_detalle)

        db.session.commit()
        return jsonify({"Message": "Repair details were successfully created"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
