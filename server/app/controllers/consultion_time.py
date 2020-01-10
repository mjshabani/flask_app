from flask import Blueprint, request, jsonify, session, render_template, abort, current_app, g
from mongoengine import DoesNotExist

from app.models.consultant import Consultant, authenticate
from app.models.consultion_time import ConsultionTime
from app.models.admin import Admin
from app.extensions import redis
from app.jsons import validate
from app.utils.uid import uid
from app.utils.pagination import paginate

api = Blueprint('api.consultion_time', __name__, url_prefix='/api/consultion_time')




@api.route('/create', methods=['POST'])
@validate('create_consultion_time')
@authenticate
def create():
    json = request.json
    if g.user_type == 'admin'
        if not 'consultant' in json:
            abort(400, error="'consultant' field is required in request body")
    elif g.user_type == 'consultant':
        json['consultant'] = g.user.id

    consultion_time = ConsultionTime()
    consultion_time.populate(json)
    consultion_time.save()
    return jsonify(consultant.to_json()), 200