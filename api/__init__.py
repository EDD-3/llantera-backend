from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_bcrypt import Bcrypt
from api.config import Config

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config())
    return app

app = create_app()
db = SQLAlchemy(app)
ma = Marshmallow(app)
bcrypt = Bcrypt(app)

from api.blueprints.exports import *

app.register_blueprint(usuario)
app.register_blueprint(index)
app.register_blueprint(empleado)
app.register_blueprint(cliente)
app.register_blueprint(vehiculo)
app.register_blueprint(inventario)
app.register_blueprint(reparacion)
app.register_blueprint(garantia)
app.register_blueprint(reparacion_detalle)
app.register_blueprint(tipo_usuario)
app.register_blueprint(parte)
app.register_blueprint(tipo_parte)

if __name__ == '__main__':
    app.run(debug=True)