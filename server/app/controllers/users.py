from flask import Blueprint, request, jsonify, session, render_template, abort

from app.models.user import User

api = Blueprint('api.users', __name__, url_prefix='/api/users')

@api.route('/register', methods=['POST'])
def register():
    json = request.json 
    user = User(name='ali', family='alavi')
    user.save()
    return jsonify(user.to_json()), 200