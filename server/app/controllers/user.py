from flask import Blueprint, request, jsonify, session, render_template, abort, current_app

from app.models.user import User
from app.extensions import redis

api = Blueprint('api.users', __name__, url_prefix='/api/users')

@api.route('/register', methods=['GET', 'POST'])
def register():
    from app.jsons import get_schema

    print(current_app.config['BASE_DIR'])
    return jsonify(get_schema('user')), 200