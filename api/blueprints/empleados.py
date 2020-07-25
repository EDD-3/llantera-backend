from flask import Flask, escape, request, Blueprint, current_app, jsonify
from json import loads as jloads
from api.models import Empleado
from api.schemas import EmpleadoSchema
from flask_cors import CORS
from api.utils import helpers

empleado = Blueprint("empleado", __name__)
empleado_schema = EmpleadoSchema()
CORS(empleado)

@empleado.route("/api/empleados", methods=["GET"])
def get_employees():
    try:
        return helpers.get_rows(Empleado,empleado_schema)
    except Exception as e:
        return jsonify({"error": str(e)}), 500



@empleado.route("/api/empleado/<id>", methods=["GET"])
def get_employee(id):
    try:
        examiner = helpers.Examiner(
            id=id,
            model=Empleado,
            schema=empleado_schema
        )
        return helpers.get_row(examiner)

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@empleado.route("/api/empleado", methods=["POST"])
def create_employee():
    try:
        examiner = helpers.Examiner(
            model=Empleado,
            schema=empleado_schema,
            unwanted_columns=["id","fecha_contratacion"],
            json_data=jloads(request.data)
        )
        return helpers.insert_row(examiner)

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@empleado.route("/api/empleado/<id>", methods=["DELETE"])
def delete_employee(id):
    try:
        examiner = helpers.Examiner(
            id=id,
            model=Empleado,
            schema=empleado_schema
        )
        return helpers.delete_row(examiner)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@empleado.route("/api/empleado/<id>", methods=["PUT"])
def update_empleado(id):
    try:
        examiner = helpers.Examiner(
            id=id,
            model=Empleado,
            schema=empleado_schema,
            unwanted_columns=["id","fecha_contratacion"],
            json_data=jloads(request.data)
        )
        return helpers.update_row(examiner)

    except Exception as e:
        return jsonify({"error": str(e)}), 500