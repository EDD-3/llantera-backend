from flask import Flask, escape, request, Blueprint, current_app, jsonify
import json

usuario = Blueprint('usuario', __name__)


@usuario.route('/api/usuario', methods=['POST'])
def get_credentials():
    log_credentials = json.loads(request.data)
