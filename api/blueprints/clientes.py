from flask import Flask, escape, request, Blueprint, current_app, jsonify
import json
from api.models import Cliente
from api.schemas import ClienteSchema
from api import bcrypt, db

cliente = Blueprint("cliente", __name__)
cliente_schema = ClienteSchema()


@cliente.route("/api/clientes", methods=["GET"])
def get_employees():
    try:
        lst_cliente = []
        for cliente in Cliente.query.all():
            lst_cliente.append(cliente_schema.dump(cliente))
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    return jsonify(lst_cliente), 200


@cliente.route("/api/cliente/<id>", methods=["GET"])
def get_employee(id):
    try:
        cliente = Cliente.query.filter_by(id=id).first()
        if not cliente:
            return jsonify({"error": "Invalid id, customer was not found"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    return cliente_schema.dump(cliente), 200


@cliente.route("/api/cliente", methods=["POST"])
def create_employee():
    try:
        nuevo_cliente = json.loads(request.data)
        cliente = Cliente(
            nombre=nuevo_cliente["nombre"],
            apellidos=nuevo_cliente["apellidos"],
            email=nuevo_cliente["email"],
            telefono=nuevo_cliente["telefono"],
        )

        db.session.add(cliente)
        db.session.commit()
        return jsonify({"Message": "Customer successfully created"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500