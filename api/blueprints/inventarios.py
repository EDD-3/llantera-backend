from flask import Flask, escape, request, Blueprint, current_app, jsonify
from api.models import Inventario
from api.schemas import InventarioSchema
from json import loads as jloads
from flask_cors import CORS
from api.utils import helpers

inventario = Blueprint("inventario", __name__)
inventario_schema = InventarioSchema()
CORS(inventario)


@inventario.route("/api/inventarios", methods=["GET"])
def get_stocks():
    try:
        return helpers.get_rows(Inventario, inventario_schema)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@inventario.route("/api/inventario/<id>", methods=["GET"])
def get_stock(id):
    try:
        examiner = helpers.Examiner(
            id=id,
            model=Inventario,
            schema=inventario_schema
        )
        return helpers.get_row(examiner)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@inventario.route("/api/inventario", methods=["POST"])
def create_stock():
    try:
        examiner = helpers.Examiner(
            model=Inventario,
            schema=inventario_schema,
            unwanted_columns=['id'],
            json_data=jloads(request.data)
        )
        return helpers.insert_row(examiner)

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@inventario.route("/api/inventario/<id>", methods=["DELETE"])
def delete_stock(id):
    try:
        examiner = helpers.Examiner(
            id=id,
            model=Inventario,
            schema=inventario_schema
        )
        return helpers.delete_row(examiner)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@inventario.route("/api/inventario/<id>", methods=["PUT"])
def update_stock(id):
    try:
        examiner = helpers.Examiner(
            id=id,
            model=Inventario,
            schema=inventario_schema,
            unwanted_columns=["id"],
            json_data=jloads(request.data)
        )
        return helpers.update_row(examiner)

    except Exception as e:
        return jsonify({"error": str(e)}), 500