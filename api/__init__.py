from flask import Flask
from api.blueprints.usuarios import usuario
from api.blueprints.index import index
from flask_sqlalchemy import SQLAlchemy


def create_app():
    app = Flask(__name__)
    app.register_blueprint(usuario)
    app.register_blueprint(index)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:d00m3r456@localhost:3307/llantera'
    return app

app = create_app()
db = SQLAlchemy(app)


if __name__ == '__main__':
    app.run(debug=True)
