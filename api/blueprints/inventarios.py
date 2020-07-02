from flask import Flask, escape, request, Blueprint, current_app, jsonify
from api.models import Inventario
from api.schemas import InventarioSchema
from api import bcrypt, db
from json import loads as jloads

inventario = Blueprint("inventario", __name__)
inventario_schema = InventarioSchema()


@inventario.route("/api/inventarios", methods=["GET"])
def get_stocks():
    try:
        lst_inventario = []
        for inventario in Inventario.query.all():
            lst_inventario.append(inventario_schema.dump(inventario))
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    return jsonify(lst_inventario), 200


@inventario.route("/api/inventario/<id>", methods=["GET"])
def get_stock(id):
    try:
        inventario = Inventario.query.filter_by(id=id).first()
        if not inventario:
            return jsonify({"error": "Invalid id, stock was not found"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    return inventario_schema.dump(inventario), 200


@inventario.route("/api/inventario", methods=["POST"])
def create_stock():
    try:
        nuevo_inventario = jloads(request.data)
        inventario = Inventario(
            nombre=nuevo_inventario["nombre"],
            apellidos=nuevo_inventario["apellidos"],
            email=nuevo_inventario["email"],
            telefono=nuevo_inventario["telefono"],
        )

        db.session.add(inventario)
        db.session.commit()
        return jsonify({"Message": "Customer successfully created"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500