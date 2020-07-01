from flask import Flask, escape, request, Blueprint, current_app, jsonify
import json

parte = Blueprint('parte', __name__)