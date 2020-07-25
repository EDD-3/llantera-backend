from flask import Flask, escape, request, Blueprint, current_app, jsonify
from api.models import Cliente
from api.schemas import ClienteSchema
from json import loads as jloads
from flask_cors import CORS
from api.utils import helpers

cliente = Blueprint("cliente", __name__)
cliente_schema = ClienteSchema()
CORS(cliente)


@cliente.route("/api/clientes", methods=["GET"])
def get_clients():
    try:
        return helpers.get_rows(Cliente, cliente_schema)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@cliente.route("/api/cliente/<id>", methods=["GET"])
def get_client(id):
    try:
        examiner = helpers.Examiner(
            id=id,
            model=Cliente,
            schema=cliente_schema
        )
        return helpers.get_row(examiner)
    except Exception as e:
        return jsonify({"error": str(e)}), 500



@cliente.route("/api/cliente", methods=["POST"])
def create_client():
    try:
        examiner = helpers.Examiner(
            model=Cliente,
            schema=cliente_schema,
            unwanted_columns=['id','fecha_registro'],
            json_data=jloads(request.data))
        return helpers.insert_row(examiner)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@cliente.route("/api/cliente/<id>", methods=["DELETE"])
def delete_client(id):
    try:
        examiner = helpers.Examiner(
            id=id,
            model=Cliente,
            schema=cliente_schema,
        )
        return helpers.delete_row(examiner)

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@cliente.route("/api/cliente/<id>", methods=["PUT"])
def update_client(id):
    try:
        examiner = helpers.Examiner(
            id=id,
            model=Cliente,
            schema=cliente_schema,
            json_data=jloads(request.data),
            unwanted_columns=["id","fecha_registro"],
        )
        return helpers.update_row(examiner)

    except Exception as e:
        return jsonify({"error": str(e)}), 500