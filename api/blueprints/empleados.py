from flask import Flask, escape, request, Blueprint, current_app, jsonify
from json import loads as jloads
from api.models import Empleado
from api.schemas import EmpleadoSchema
from api import bcrypt, db
from flask_cors import CORS

empleado = Blueprint("empleado", __name__)
empleado_schema = EmpleadoSchema()
CORS(empleado)

@empleado.route("/api/empleados", methods=["GET"])
def get_employees():
    try:
        empleados = []

        for empleado in Empleado.query.all():
            empleados.append(empleado_schema.dump(empleado))

        if len(empleados) == 0:
            return jsonify({"error": "No employees in database"}), 404

    except Exception as e:
        return jsonify({"error": str(e)}), 500

    return jsonify(empleados), 200


@empleado.route("/api/empleado/<id>", methods=["GET"])
def get_employee(id):
    try:
        empleado = Empleado.query.filter_by(id=id).first()

        if empleado is not None:
            return empleado_schema.dump(empleado), 200

        else:
            return jsonify({"error": "Invalid id, employee was not found"}), 400

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@empleado.route("/api/empleado", methods=["POST"])
def create_employee():
    try:
        nuevo_empleado = jloads(request.data)
        table_columns = [
            column.name
            for column in Empleado.__table__.columns
            if column.name != "id" and column.name != "fecha_contratacion"
        ]

        for field in nuevo_empleado:
            if field in table_columns:
                table_columns.remove(field)

        if len(table_columns) == 0:
            empleado = Empleado(
                nombre=nuevo_empleado["nombre"],
                apellidos=nuevo_empleado["apellidos"],
                email=nuevo_empleado["email"],
                telefono=nuevo_empleado["telefono"],
                direccion=nuevo_empleado["direccion"],
            )

            db.session.add(empleado)
            db.session.commit()
            nuevo_empleado = Empleado.query.order_by(Empleado.id.desc()).first()

        else:
            return jsonify({"missing fields": table_columns}), 400

    except Exception as e:
        return jsonify({"error": str(e)}), 500

    return empleado_schema.dump(nuevo_empleado), 200


@empleado.route("/api/empleado/<id>", methods=["DELETE"])
def delete_empleado(id):
    try:
        empleado = Empleado.query.filter_by(id=id).first()

        if empleado is not None:
            db.session.delete(empleado)
            db.session.commit()

        else:
            return jsonify({"error": "Invalid id, employee not found"}), 404

    except Exception as e:
        return jsonify({"error": str(e)}), 500

    return jsonify({"message": "Success"}), 200


@empleado.route("/api/empleado/<id>", methods=["PUT"])
def update_empleado(id):
    try:
        update_dict = jloads(request.data)
        table_columns = [
            column.name for column in Empleado.__table__.columns if column.name != "id" and column.name != "fecha_contratacion"
        ]
        empleado = Empleado.query.filter_by(id=id).first()

        for field in update_dict:

            if field in table_columns:
                table_columns.remove(field)

        if empleado is not None:
            if len(table_columns) == 0:
                Empleado.query.filter_by(id=id).update(update_dict)
                db.session.commit()

            else:
                return jsonify({"missing fields": table_columns}),400

        else:
            return jsonify({"error": "Invalid id, employee not found"}), 404

    except Exception as e:
        return jsonify({"error": str(e)}), 500

    return ({"message": "Success"}), 200
