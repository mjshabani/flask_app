from flask import Blueprint, request, jsonify, session, render_template, abort, current_app, g
from mongoengine import DoesNotExist

from app.models.consultant import Consultant, authenticate
from app.models.admin import Admin
from app.extensions import redis
from app.jsons import validate
from app.utils.uid import uid
from app.utils.pagination import paginate
from app.utils.user_type import UserType

api = Blueprint('api.consultant', __name__, url_prefix='/api/consultant')




@api.route('/create', methods=['POST'])
@validate('create_consultant')
@Admin.authenticate
def create():
    consultant = Consultant()
    consultant.username=request.json['username']
    consultant.password=request.json['password']
    consultant.save()
    return jsonify(consultant.to_json()), 200


@api.route('/login', methods=['POST'])
@validate('create_consultant')
def login():
    json = request.json
    try:
        consultant = Consultant.objects.get(username=json['username'])
        if consultant.check_password(json['password']):
            access_token = uid()
            redis.set('cat%s' % access_token, consultant.id, current_app.config['CONSULTANT_ACCESS_TOKEN_TIMEOUT'])
            result = consultant.to_json()
            result['access_token'] = access_token
            return jsonify(result), 201
        else:
            abort(401)
    except DoesNotExist:
        abort(401)

@api.route('/<string:consultant_id>/update', methods=['PUT'])
@validate('update_consultant')
@authenticate
def update(consultant_id):
    json = request.json
    if g.user_type == UserType.CONSULTANT and g.user.id != consultant_id:
        abort(400)
    consultant = Consultant.objects.get(id=consultant_id)
    consultant.populate(json)
    consultant.save()
    return jsonify(consultant.to_json()), 200


@api.route('', methods=['GET'])
@paginate
def get_list():
    list = Consultant.objects
    # if not g.user_type == UserType.ADMIN: # TODO for deactived consultant
    #     list = list.filter()
    return list