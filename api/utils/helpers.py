from flask import jsonify
from api import db

class Examiner(object):
    __slots__=['id','model','schema','unwanted_columns','json_data']
    def __init__(self,id=None,model=None,schema=None,unwanted_columns=None, json_data=None):
        self.id = id
        self.model = model
        self.schema = schema
        self.unwanted_columns = unwanted_columns
        self.json_data = json_data


def get_rows(model, schema):
    return jsonify([ schema.dump(m) for m in model.query.all() ])

def get_row(examiner):
    row = examiner.model.query.filter_by( id=examiner.id ).first()

    if row is not None:
        return examiner.schema.dump(row),200
    else:
        return jsonify({"error": "Invalid id, row was not found"}), 404

def delete_row(examiner):
    row = examiner.model.query.filter_by( id=examiner.id ).first()

    if row is not None:
        db.session.delete(row)
        db.session.commit()
        return examiner.schema.dump(row), 200

    else:
        return jsonify({"error": "Invalid id, row was not found"}), 404

def update_row(examiner):

    missing_fields,examiner.json_data = verify_fields( examiner.json_data, examiner.model, examiner.unwanted_columns )
    
    if len(missing_fields) == 0:
        row = examiner.model.query.filter_by( id=examiner.id ).first()

        if row is not None:
            examiner.model.query.filter_by( id=examiner.id ).update(examiner.json_data)
            db.session.commit()
            row = examiner.model.query.filter_by( id=examiner.id ).first()
            return examiner.schema.dump(row)

        else:
            return jsonify({"error": "Invalid id, row not found"}), 404

    else:
         return jsonify({"missing fields": missing_fields}), 400

def insert_row(examiner):

    missing_fields,examiner.json_data = verify_fields( examiner.json_data, examiner.model, examiner.unwanted_columns )
    if len(missing_fields) == 0:
        new_model = examiner.model(**examiner.json_data)
        db.session.add(new_model)
        db.session.commit()
        new_model = examiner.model.query.order_by(
                examiner.model.id.desc()
            ).first()
        return examiner.schema.dump(new_model)

    else:
        return jsonify({"missing fields": missing_fields}), 400


def verify_fields(json_data, model, unwanted_columns):

    table_columns = [
            column.name
            for column in frozenset(model.__table__.columns)
            if column.name not in unwanted_columns
        ]
    
    new_dict = {
                key:val 
                for key, val in json_data.items() 
                if key in table_columns
        }

    table_columns = set(table_columns) - set(new_dict)

    return table_columns, new_dict