from flask import Blueprint, request, jsonify, session, render_template, abort, current_app
from app.models.admin import Admin
from app.extensions import redis
from app.jsons import validate
from app.utils.uid import uid
from mongoengine import DoesNotExist

api = Blueprint('api.admin', __name__, url_prefix='/api/admin')

@api.route('/login', methods=['POST'])
@validate('login_admin')
def login():
    json = request.json
    try:
        admin = Admin.objects.get(username=json['username'])
        if admin.check_password(json['password']):
            secret_key = uid()
            redis.set('ask%s' % secret_key, admin.username, current_app.config['SECRET_KEY_TIMEOUT'])
            return jsonify(admin=admin.username, secret_key=secret_key), 201
        else:
            abort(401)
    except DoesNotExist:
        abort(401)