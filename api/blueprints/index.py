from flask import Flask, escape, request, Blueprint

index = Blueprint('index', __name__)


@index.route('/')
def hello():
    name = 'World'
    return f'Hello, {escape(name)}!'