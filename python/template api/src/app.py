import sys
sys.path.append('../')
sys.path.insert(0, './')
from flask import Flask
from flask_restful import Api
from flask_jwt import JWT
from authentication.auth import verify, identity, UserProfile, CreateProfile
from database import DbRepositor

app = Flask(__name__)
app.config['SECRET_KEY'] = 'super-secret'

api = Api(app, prefix="/api/v1")
jwt = JWT(app, verify, identity)
db = DbRepositor()
db.openDb()

api.add_resource(UserProfile, '/Profile')
api.add_resource(CreateProfile, '/Profile/create')

if __name__ == '__main__':
    app.run(debug=True)
