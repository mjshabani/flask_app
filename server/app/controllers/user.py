from flask import Blueprint, request, jsonify, session, render_template, abort, current_app
from app.models.user import User
from app.extensions import redis
from app.jsons import validate

api = Blueprint('api.user', __name__, url_prefix='/api/user')




@api.route('/register', methods=['GET', 'POST'])
@validate('user')
def register():
    from app.jsons import get_schema

    return jsonify(get_schema('user')), 200