from flask import Flask, escape, request, Blueprint, current_app, jsonify
import json
from api.models import Parte
from api.schemas import ParteSchema
from api import bcrypt, db

parte = Blueprint("parte", __name__)
parte_schema = ParteSchema()


@parte.route("/api/partes", methods=["GET"])
def get_parts():
    try:
        lst_parte = []
        for parte in Parte.query.all():
            lst_parte.append(parte_schema.dump(parte))
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    return jsonify(lst_parte), 200


@parte.route("/api/parte/<id>", methods=["GET"])
def get_part(id):
    try:
        parte = Parte.query.filter_by(id=id).first()
        if not parte:
            return jsonify({"error": "Invalid id, customer was not found"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    return parte_schema.dump(parte), 200


@parte.route("/api/parte", methods=["POST"])
def create_part():
    try:
        nuevo_parte = json.loads(request.data)
        parte = Parte(
            nombre_parte=nuevo_parte["nombre_parte"],
            tipo_parte_id=nuevo_parte["tipo_parte_id"],
            descripcion_parte=nuevo_parte["descripcion_parte"],
            precio=nuevo_parte["precio"],
        )

        db.session.add(parte)
        db.session.commit()
        return jsonify({"Message": "Customer successfully created"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500