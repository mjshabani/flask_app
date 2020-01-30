from flask import Blueprint, request, jsonify, session, render_template, abort, current_app, g, abort
from mongoengine import DoesNotExist

from app.models.user import User, authenticate
from app.models.consultant import Consultant
from app.models.consultation_time import ConsultationTime
from app.models.admin import Admin
from app.models.reservation import Reservation

from app.jsons import validate
from app.utils.uid import uid
from app.utils.pagination import paginate
from app.utils.user_type import UserType

api = Blueprint('api.reservation', __name__, url_prefix='/api/reservation')


@api.route('', methods=['POST'])
@validate('create_reservation')
@authenticate
def create():
    json = request.json
    if g.user_type == UserType.ADMIN:
        abort(400, 'This request is accessible only for normal user.')

    reservation = Reservation()
    reservation.populate(json)
    reservation.save()
    return jsonify(reservation.to_json()), 201

@api.route('/<string:reservation_id>', methods=['GET'])
def get(reservation_id):
    reservation = Reservation.objects.get_or_404(id=reservation_id)

    if Admin.check_admin() \
        or (User.check_user() and g.user.id == reservation.user.id) \
        or (Consultant.check_user and g.user.id == reservation.consultation_time.consultant.id):

        return jsonify(reservation.to_json())
    else:
        abort(400, 'The reservation is not accessible for you!')

@api.route('/<string:reservation_id>', methods=['DELETE'])
@authenticate
def delete(reservation_id):
    reservation = Reservation.objects.get_or_404(id=reservation_id)

    if g.user_type == UserType.USER and g.user.id != reservation.user.id:
        abort(401, 'This reservation is for another user.')

    reservation.delete()
    return jsonify(), 200


@api.route('', methods=['GET'])
@paginate
def get_list():
    args = request.args
    list = Reservation.objects

    consultant_id = args.get('consultant', None)
    user_id = args.get('user', None)

    if user_id:
        user = User.objects.get_or_404(id=user_id)
        list = list.filter(user=user)

    if consultant_id:
        consultant = Consultant.objects.get_or_404(id=consultant_id)
        consultation_times = ConsultationTime.objects.filter(consultant=consultant).all()
        list = list.filter(consultant_time__in=consultation_times)

    return list