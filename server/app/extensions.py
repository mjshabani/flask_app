from flask_mongoengine import MongoEngine
from flask_redis import FlaskRedis
from flask_json_schema import JsonSchema

mongoengine = MongoEngine()
redis = FlaskRedis()
jsonschema = JsonSchema()