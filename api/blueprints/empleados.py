from flask import Flask, escape, request, Blueprint, current_app, jsonify
import json
from api.models import Empleado
from api.schemas import EmpleadoSchema
from api import bcrypt, db

empleado = Blueprint("empleado", __name__)
empleado_schema = EmpleadoSchema()


@empleado.route("/api/empleados", methods=["GET"])
def get_employees():
    try:
        lst_empleado = []
        for empleado in Empleado.query.all():
            lst_empleado.append(empleado_schema.dump(empleado))
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    return jsonify(lst_empleado), 200


@empleado.route("/api/empleado/<id>", methods=["GET"])
def get_employee(id):
    try:
        empleado = Empleado.query.filter_by(id=id).first()
        if not empleado:
            return jsonify({"error": "Invalid id, employee was not found"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    return empleado_schema.dump(empleado), 200


@empleado.route("/api/empleado", methods=["POST"])
def create_employee():
    try:
        nuevo_empleado = json.loads(request.data)
        empleado = Empleado(
            nombre=nuevo_empleado["nombre"],
            apellidos=nuevo_empleado["apellidos"],
            email=nuevo_empleado["email"],
            telefono=nuevo_empleado["telefono"],
            direccion=nuevo_empleado["direccion"],
        )

        db.session.add(empleado)
        db.session.commit()
        return jsonify({"Message": "Employee successfully created"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
