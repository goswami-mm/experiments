from flask import jsonify, request
from flask_restful import Resource
from flask_restful.reqparse import RequestParser
from database import DbRepositor, User
from jwt import ExpiredSignature, DecodeError
import jwt
import datetime

subscriber_request_parser = RequestParser(bundle_errors=True)
subscriber_request_parser.add_argument("name", type=str, required=True, help="Name has to be valid string")
subscriber_request_parser.add_argument("password", required=True)
subscriber_request_parser.add_argument("phone", type=int, required=True, help="Please enter valid phone")

auth_request_parser = RequestParser(bundle_errors=True)
auth_request_parser.add_argument("name", type=str, required=True, help="Name has to be valid string")
auth_request_parser.add_argument("password", required=True)

SECRET_KEY = "my_secret_key"


def verify(username, password):
    if not (username and password):
        return False
    return DbRepositor().validUser(username, password)


def identity(token):
    try:
        print("token", token)
        decoded_payload = jwt.decode(jwt=token, key=SECRET_KEY)
        print(decoded_payload)
        return int(decoded_payload.get('uid'))
    except DecodeError as e:
        return {"Error": e}
    except ExpiredSignature as e:
        return {"Signature Error": e}
    except:
        return {"Error"}


class UserProfile(Resource):
    def get(self):
        current_identity = identity(request.headers.get('jwtToken'))
        print(current_identity)
        if current_identity:
            return jsonify(DbRepositor().getUser(current_identity))
        else:
            return jsonify(current_identity.__str__())


class UserAuth(Resource):
    def post(self):
        args = auth_request_parser.parse_args()
        user = verify(args.name, args.password)
        print(user)
        if user:
            payload = {
                "uid": user.id,
                "name": user.name,
                "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=10)
            }
            return {"token": jwt.encode(payload=payload, key=SECRET_KEY).__str__()}
        else:
            return {"error": "Auth Failed"}


class CreateProfile(Resource):
    def post(self):
        args = subscriber_request_parser.parse_args()
        DbRepositor().addUser(User(1, name=args.name, password=args.password, phone=args.phone))
        return {"msg": "User added", "user_data": args}
