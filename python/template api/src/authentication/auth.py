from flask import jsonify
from flask_restful import Resource, Api
from flask_jwt import JWT, jwt_required, current_identity
from flask_restful.reqparse import RequestParser
from database import DbRepositor, User

users = [{"masnun": "abc123"}]
USER_ID = {"masnun": "abc123"}

subscriber_request_parser = RequestParser(bundle_errors=True)
subscriber_request_parser.add_argument("name", type=str, required=True, help="Name has to be valid string")
subscriber_request_parser.add_argument("password", required=True)
subscriber_request_parser.add_argument("phone", type=int, required=True, help="Please enter valid phone")


def verify(username, password):
    if not (username and password):
        return False
    return DbRepositor().validUser(username, password)


def identity(payload):
    return payload['identity']


class UserProfile(Resource):
    @jwt_required()
    def get(self):
        return jsonify(DbRepositor().getUser(current_identity))


class CreateProfile(Resource):
    def post(self):
        args = subscriber_request_parser.parse_args()
        DbRepositor().addUser(User(1, name=args.name, password=args.password, phone=args.phone))
        return {"msg": "User added", "user_data": args}
