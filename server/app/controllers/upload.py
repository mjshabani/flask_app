import os
from flask import Flask, abort, Blueprint, jsonify, request, redirect, url_for, current_app, send_from_directory
from app.utils.uid import uid

ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

api = Blueprint('api.upload', __name__, url_prefix='/api/upload')


@api.route('', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        print('not found')
        abort(400)
    file = request.files['file']
    if file.filename == '':
        abort(400)
    filename = uid() + ".jpg"
    file.save(os.path.join(current_app.config['UPLOAD_DIR'], filename))
    return jsonify({"url" :url_for( "api.upload.download_file", filename=filename, _external=True)})


@api.route('/<path:filename>', methods=['GET'])
def download_file(filename):
    return send_from_directory(directory=current_app.config['UPLOAD_DIR'], filename=filename)