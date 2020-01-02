from flask import Blueprint, request, jsonify, session, render_template

api = Blueprint('api.users', __name__, url_prefix='/api/users')

@api.route('/register', methods=('GET', 'POST'))
def register():
    return render_template('auth/register.html')