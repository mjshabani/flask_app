from flask import Blueprint, request, jsonify, session, render_template, abort, current_app, g
from mongoengine import DoesNotExist

from app.models.consultant import Consultant, authenticate
from app.models.consultation_time import ConsultationTime, Status
from app.models.admin import Admin
from app.extensions import redis
from app.jsons import validate

from app.utils.uid import uid
from app.utils.pagination import paginate
from app.utils.datetime import string_to_datetime
from app.utils.user_type import UserType

api = Blueprint('api.consultation_time', __name__, url_prefix='/api/consultation_time')

@api.route('/create', methods=['POST'])
@validate('create_consultation_time')
@authenticate
def create():
    json = request.json
    if g.user_type == UserType.ADMIN:
        if not 'consultant' in json:
            abort(400, "'consultant' field is required in request body")
    elif g.user_type == UserType.CONSULTANT:
        json['consultant'] = g.user.id

    consultation_time = ConsultationTime()
    consultation_time.populate(json)
    consultation_time.status = int(Status.FREE)
    consultation_time.save()
    return jsonify(consultation_time.to_json()), 200

@api.route('/<string:consultation_time_id>', methods=['GET'])
def get(consultation_time_id):
    consultation_time = ConsultationTime.objects.get_or_404(id=consultation_time_id)
    return jsonify(consultation_time.to_json()), 200

@api.route('', methods=['GET'])
@paginate
def get_list():
    args = request.args
    list = ConsultationTime.objects

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

@api.route('/<string:consultation_time_id>', methods=['DELETE'])
@authenticate
def delete(consultation_time_id):
    consultation_time = ConsultationTime.objects.get_or_404(id=consultation_time_id)
    if g.user_type == UserType.CONSULTANT and g.user.id != consultation_time.consultant.id:
        abort(401, 'The consultation time is not for you!')

    if consultation_time.status == Status.FREE:
        consultation_time.delete()
        return jsonify(), 200
    else:
        return abort(400, 'The consultation time is reserved.')