from flask import Blueprint, request, jsonify, session, render_template, abort, current_app, g
from mongoengine import DoesNotExist

from app.models.consultant import Consultant, authenticate
from app.models.consultion_time import ConsultionTime, Status
from app.models.admin import Admin
from app.extensions import redis
from app.jsons import validate

from app.utils.uid import uid
from app.utils.pagination import paginate
from app.utils.datetime import string_to_datetime

api = Blueprint('api.consultion_time', __name__, url_prefix='/api/consultion_time')

@api.route('/create', methods=['POST'])
@validate('create_consultion_time')
@authenticate
def create():
    json = request.json
    if g.user_type == 'admin':
        if not 'consultant' in json:
            abort(400, "'consultant' field is required in request body")
    elif g.user_type == 'consultant':
        json['consultant'] = g.user.id

    consultion_time = ConsultionTime()
    consultion_time.populate(json)
    consultion_time.status = int(Status.Free)
    consultion_time.save()
    return jsonify(consultion_time.to_json()), 200

@api.route('', methods=['GET'])
@paginate
def get_list():
    args = request.args
    list = ConsultionTime.objects

    consultant_id = args.get('consultant', None)
    begin_time__lte = args.get('begin_time__lte', None)
    begin_time__gte = args.get('begin_time__gte', None)
    status = args.get('status', None, type=int)

    if consultant_id:
        consultant = Consultant.objects.get_or_404(id=consultant_id)
        list = list.filter(consultant=consultant)

    if begin_time__lte:
        try:
            list = list.filter(begin_time__lte=string_to_datetime(begin_time__lte))
        except:
            abort(400, "invalid 'begin_time__lte'")
    
    if begin_time__gte:
        try:
            list = list.filter(begin_time__gte=string_to_datetime(begin_time__gte))
        except:
            abort(400, "invalid 'begin_time__gte'")

    if status != None:
        list = list.filter(status=status)

    
    return list