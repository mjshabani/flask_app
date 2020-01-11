from flask import Blueprint, request, jsonify, session, render_template, abort, current_app, g
from mongoengine import DoesNotExist

from app.models.user import User, authenticate
from app.models.reservation import Reservation

from app.jsons import validate
from app.utils.uid import uid
from app.utils.user_type import UserType

api = Blueprint('api.reservation', __name__, url_prefix='/api/reservation')


@api.route('/create', methods=['POST'])
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