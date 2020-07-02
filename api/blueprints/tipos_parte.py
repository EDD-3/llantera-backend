from flask import Flask, escape, request, Blueprint, current_app, jsonify
import json
from api.models import TipoParte
from api.schemas import TipoParteSchema
from api import bcrypt, db

tipo_parte = Blueprint("tipo_parte", __name__)
tipo_parte_schema = TipoParteSchema()


@tipo_parte.route("/api/tiposParte", methods=["GET"])
def get_parts():
    try:
        lst_tipo_parte = []
        for tipo_parte in TipoParte.query.all():
            lst_tipo_parte.append(tipo_parte_schema.dump(tipo_parte))
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    return jsonify(lst_tipo_parte), 200


@tipo_parte.route("/api/tipoParte/<id>", methods=["GET"])
def get_part(id):
    try:
        tipo_parte = TipoParte.query.filter_by(id=id).first()
        if not tipo_parte:
            return jsonify({"error": "Invalid id, customer was not found"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    return tipo_parte_schema.dump(tipo_parte), 200


@tipo_parte.route("/api/tipoParte", methods=["POST"])
def create_part():
    try:
        nuevo_tipo_parte = json.loads(request.data)
        tipo_parte = TipoParte(
            denominacion_parte=nuevo_tipo_parte["denominacion_parte"],
            descripcion_tipo_parte=nuevo_tipo_parte["descripcion_tipo_parte"],

        )

        db.session.add(tipo_parte)
        db.session.commit()
        return jsonify({"Message": "Customer successfully created"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500