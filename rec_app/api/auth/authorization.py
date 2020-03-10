import datetime
import logging

from flask import request
from flask_restplus import Resource
from flask_jwt_extended import create_access_token

from rec_app.api.restplus import api
from rec_app.database.models.user_model import User

log = logging.getLogger(__name__)

# ns = Namespace('auth', description='Operations related to user authentication')
ns = api.namespace('auth', description='Operations related to user authentication')

JWT_TOKEN_TTL = 100


@ns.route("/login")
class Login(Resource):

    def get(self):
        return {"message": "Only Http POST is supported for this route."}

    @api.doc(params={'email': 'Registered email', 'password': 'Valid password'})
    def post(self):
        if request.is_json:
            email = request.json['email']
            password = request.json['password']
        else:
            email = request.form['email']
            password = request.form['password']

        user = User.query.filter_by(email=email).first()
        if user:
            valid_user = True if user.verify_password(password) else False
            if valid_user:
                user_identity = {"email": user.email, "user_id": user.user_id}
                access_token = create_access_token(identity=user_identity,
                                                   expires_delta=datetime.timedelta(seconds=JWT_TOKEN_TTL))
                full_name = user.first_name + " " + user.last_name
                return {"message": "Login succeeded!", "access_token": access_token, "fullName": full_name}
            return {"message": "Bad email or password"}, 401
        else:
            return {"message": "Bad email or password"}, 401


@ns.route("/register")
class Register(Resource):
    first_name = last_name = user_name = email = password = ''

    def get(self):
        return {"message": "Only Http POST is supported for this route."}

    @api.doc(params={'firstName': 'Usre\'s first name', 'lastName': 'User\'s last name', 'userName': 'unique username',
                     'email': 'Valid email', 'password': 'Valid password'})
    def post(self):
        if request.is_json:
            first_name = request.json['firstName']
            last_name = request.json['lastName']
            username = request.json['userName']
            email = request.json['email']
            password = request.json['password']
        else:
            first_name = request.form['firstName']
            last_name = request.form['lastName']
            username = request.form['userName']
            email = request.form['email']
            password = request.form['password']

        email_exist = User.query.filter_by(email=email).first()
        if email_exist:
            return {"message": "That email already exists. Please try with another email."}, 409
        User.add_user(first_name, last_name, username, email, password)
        return {"message": "User created successfully."}, 201
