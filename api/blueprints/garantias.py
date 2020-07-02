from flask import Flask, escape, request, Blueprint, current_app, jsonify
from api.models import Garantia
from api.schemas import GarantiaSchema
from api import bcrypt, db
from json import loads as jloads

garantia = Blueprint("garantia", __name__)
garantia_schema = GarantiaSchema()


@garantia.route("/api/garantias", methods=["GET"])
def get_warranties():
    try:
        lst_garantia = []
        for garantia in Garantia.query.all():
            lst_garantia.append(garantia_schema.dump(garantia))
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    return jsonify(lst_garantia), 200


@garantia.route("/api/garantia/<id>", methods=["GET"])
def get_warranty(id):
    try:
        garantia = Garantia.query.filter_by(id=id).first()
        if not garantia:
            return jsonify({"error": "Invalid id, warranty was not found"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    return garantia_schema.dump(garantia), 200


@garantia.route("/api/garantia", methods=["POST"])
def create_warranty():
    try:
        nuevo_garantia = jloads(request.data)
        garantia = Garantia()
        db.session.add(garantia)
        db.session.commit()
        return jsonify({"Message": "Warranty successfully created"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500