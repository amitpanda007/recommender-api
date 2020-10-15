import datetime
import logging

from flask import request
from flask_restplus import Resource
from flask_jwt_extended import create_access_token

from rec_app.api.auth.auth import authenticate_user, AuthenticationError, auth_refresh_required, refresh_authentication
from rec_app.api.restplus import api
from rec_app.database.models.recommendations_model import RecommendationsModel, RecommendationsEnum
from rec_app.database.models.user_model import UserModel

log = logging.getLogger(__name__)

# ns = Namespace('auth', description='Operations related to user authentication')
ns = api.namespace('auth', description='Operations related to user authentication')


@ns.route("/login")
class Login(Resource):
    """
    Login user
    """

    def get(self):
        return {"message": "Only Http POST is supported for this route."}

    @api.doc(params={'email': 'Registered email', 'password': 'Valid password'})
    def post(self):
        try:
            if request.is_json:
                email = request.json.get('email')
                password = request.json.get('password')
            else:
                email = request.form['email']
                password = request.form['password']

            access_token, refresh_token, full_name = authenticate_user(email, password)
            return {"message": "Login succeeded!", "accessToken": access_token, 'refreshToken': refresh_token,
                    "fullName": full_name}

        except AuthenticationError as error:
            return {"message": "Bad email or password"}, 403


# TODO:  implement deletion of access token
@ns.route("/logout")
class Logout(Resource):

    def get(self):
        pass


@ns.route("/register")
class Register(Resource):
    first_name = last_name = user_name = email = password = ''

    def get(self):
        return {"message": "Only Http POST is supported for this route."}

    @api.doc(params={'firstName': 'Usre\'s first name', 'lastName': 'UserModel\'s last name', 'userName': 'unique username',
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

        email_exist = UserModel.query.filter_by(email=email).first()
        if email_exist:
            return {"message": "That email already exists. Please try with another email."}, 409

        UserModel.add_user(first_name, last_name, username, email, password)
        user = UserModel.query.filter_by(email=email).first()
        RecommendationsModel.init_recommendation(user.user_id, RecommendationsEnum.MATRIX_FACTORIZATION, RecommendationsEnum.EMPTY_STATUS, None)
        RecommendationsModel.init_recommendation(user.user_id, RecommendationsEnum.SINGULAR_VALUE_DECOMPOSITION, RecommendationsEnum.EMPTY_STATUS, None)
        return {"message": "User created successfully."}, 201


@ns.route("/refresh")
class Refresh(Resource):
    """
    Login user
    """

    def get(self):
        return {"message": "Only Http POST is supported for this route."}

    @api.doc(params={'email': 'Registered email', 'password': 'Valid password'})
    @auth_refresh_required
    def post(self):
        try:
            access_token = refresh_authentication()
            return {'accessToken': access_token}
        except AuthenticationError as error:
            return {"message": "Bad email or password"}, 403