from functools import wraps
import os, re
import json as j
from glob import glob
from flask import request, current_app
from app.extensions import jsonschema

jsonschema_classes = [
    'AdminLogin',
    'CreateConsultant', 'UpdateConsultant',
    'CreateConsultionTime',
    'User',
]

jsonschema_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../jsonschema')

def write_schemas_to_file():
    pattern = os.path.join(os.path.dirname(os.path.abspath(__file__)), "*.py")
    for file in glob(pattern):
        name = os.path.splitext(os.path.basename(file))[0]
        module = __import__('app.jsons.%s' % name, fromlist=[''])
        for item in dir(module):
            if item in jsonschema_classes:
                jsl_class = getattr(module, item)
                path = os.path.join(jsonschema_path, camel_to_underscore(item) + '.json')
                with open(path ,'w') as file:
                    file.write(j.dumps(jsl_class.get_schema()))
            


def get_schema(jsonschema_name):
    try:
        path = os.path.join(jsonschema_path, jsonschema_name + '.json')
        with open(path) as file:
            string = file.read()
            jsonschema = j.loads(string)
        return jsonschema
    except:
        return {}
        

def validate(jsonschema_name):
    return jsonschema.validate(get_schema(jsonschema_name))

def camel_to_underscore(string):
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', string)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()