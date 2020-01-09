from flask import Blueprint, request, jsonify, session, render_template, abort, current_app
from app.models.consultant import Consultant
from app.models.admin import Admin
from app.extensions import redis
from app.jsons import validate

api = Blueprint('api.consultant', __name__, url_prefix='/api/consultant')




@api.route('/create', methods=['POST'])
@validate('create_consultant')
@Admin.authenticate
def create():
    consultant = Consultant()
    consultant.username = request.json['username']
    consultant.password = request.json['password']
    consultant.save()
    return jsonify(consultant.to_json()), 200