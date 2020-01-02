from functools import wraps
import os
from flask import request, current_app
from app.extensions import jsonschema

jsons = ['user']

def get_schema(jsonschema_name):
    import json as j
    jsonschema_dir = current_app.config['JSONSCHEMA_DIR']
    path = os.path.join(jsonschema_dir, jsonschema_name + '.json')
    with open(path) as file:
        string = file.read()
        jsonschema = j.loads(string)
    return jsonschema
        

def validate(jsonschema_name):
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwds):
            #TODO
            jsonschema.validate(jsonschema)
            return f(*args, **kwds)
        return wrapper