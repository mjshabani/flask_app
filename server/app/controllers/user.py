from flask import Blueprint, request, jsonify, session, render_template, abort, current_app, g
from random import randint
from mongoengine import DoesNotExist

from app.models.user import User, authenticate
from app.extensions import redis
from app.jsons import validate
from app.utils.uid import uid

api = Blueprint('api.user', __name__, url_prefix='/api/user')

@api.route('/register', methods=['POST'])
@validate('register_user')
def register():
    json = request.json

    user = User()
    user.phone_number = json['phone_number']
    user.username = json['username']
    user.password = uid()[:20]
    user.save()
    short_code = f'{randint(1, 10**5):05}' if not current_app.config['DEBUG'] else '12321'
    long_code = uid()

    redis.set('utt%s%s' %(long_code, short_code), user.id, current_app.config['USER_TEMP_TOKEN_TIMEOUT'])
    result = {
        'phone_number' : user.phone_number,
        'username' : user.username,
        'long_code' : long_code
    }
    # send short_code to phone number

    return jsonify(result), 201

@api.route('/verify', methods=['PUT'])
@validate('verify_user')
def verify():
    json = request.json
    
    user_id = redis.get('utt%s%s' %(json['long_code'], json['short_code']))

    if not user_id:
        abort(401, 'The code is expired.')
    user = User.objects.get_or_404(id=user_id)
    access_token = uid()
    redis.set('uat%s' % access_token, user.id, current_app.config['USER_ACCESS_TOKEN_TIMEOUT'])

    result = user.to_json()
    result['access_token'] = access_token

    return jsonify(result), 200

@api.route('/change_password', methods=['PUT'])
@validate('change_password')
@authenticate
def change_password():
    json = request.json
    g.user.password = json['password']

    g.user.save()    
    return jsonify(g.user.to_json()), 200

@api.route('/login', methods=['POST'])
@validate('login_user')
def login():
    json = request.json
    try:
        user = User.objects.get(username=json['username'])
        if user.check_password(json['password']):
            access_token = uid()
            redis.set('uat%s' % access_token, user.id, current_app.config['USER_ACCESS_TOKEN_TIMEOUT'])
            result = user.to_json()
            result['access_token'] = access_token
            return jsonify(result), 201
        else:
            abort(401)
    except DoesNotExist:
        abort(401)