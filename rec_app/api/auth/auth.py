# example code from https://github.com/keathmilligan/angular-jwt-flask

"""
Authentication Functions
"""
import datetime
from functools import wraps
from flask import abort
from flask_jwt_extended import (
    create_access_token, create_refresh_token, get_jwt_identity,
    verify_jwt_in_request, verify_jwt_refresh_token_in_request
)

from rec_app.database.models.user_model import UserModel

JWT_ACC_TOKEN_TTL = 14400
JWT_REF_TOKEN_TTL = 86400


class AuthenticationError(Exception):
    """Base Authentication Exception"""
    def __init__(self, msg=None):
        self.msg = msg

    def __str__(self):
        return self.__class__.__name__ + '(' + str(self.msg) + ')'


class InvalidCredentials(AuthenticationError):
    """Invalid username/password"""


class AccountInactive(AuthenticationError):
    """Account is disabled"""


class AccessDenied(AuthenticationError):
    """Access is denied"""


class UserNotFound(AuthenticationError):
    """User identity not found"""


def authenticate_user(email, password):
    """
    Authenticate a user
    """

    user = UserModel.query.filter_by(email=email).first()
    if user:
        valid_user = True if user.verify_password(password) else False
        if valid_user:
            user_identity = {"email": user.email, "user_id": user.user_id}
            full_name = user.first_name + " " + user.last_name
            return (
                create_access_token(identity=user_identity, expires_delta=datetime.timedelta(seconds=JWT_ACC_TOKEN_TTL)),
                create_refresh_token(identity=user_identity, expires_delta=datetime.timedelta(seconds=JWT_REF_TOKEN_TTL)),
                full_name
            )
        else:
            raise AccountInactive(email)
    else:
        raise InvalidCredentials()


def get_authenticated_user():
    """
    Get authentication token user identity and verify account is active
    """
    identity = get_jwt_identity()
    user = UserModel.query.filter_by(email=identity.get('email')).first()
    if user:
        return user.email, user.user_id
    else:
        raise UserNotFound(identity)


def deauthenticate_user():
    """
    TODO : Add database changes to mark user logout activity
    Log user out
    in a real app, set a flag in user database requiring login, or
    implement token revocation scheme
    """
    identity = get_jwt_identity()


def refresh_authentication():
    """
    Refresh authentication, issue new access token
    """
    email, user_id = get_authenticated_user()
    user_identity = {"email": email, "user_id": user_id}
    return create_access_token(identity=user_identity, expires_delta=datetime.timedelta(seconds=JWT_ACC_TOKEN_TTL))


def auth_required(func):
    """
    View decorator - require valid access token
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        verify_jwt_in_request()
        try:
            get_authenticated_user()
            return func(*args, **kwargs)
        except (UserNotFound, AccountInactive) as error:
            abort(403)
    return wrapper


def auth_refresh_required(func):
    """
    View decorator - require valid refresh token
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        verify_jwt_refresh_token_in_request()
        try:
            get_authenticated_user()
            return func(*args, **kwargs)
        except (UserNotFound, AccountInactive) as error:
            abort(403)
    return wrapper


def admin_required(func):
    """
    View decorator - required valid access token and admin access
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        verify_jwt_in_request()
        try:
            user = get_authenticated_user()
            if user['is_admin']:
                return func(*args, **kwargs)
            else:
                abort(403)
        except (UserNotFound, AccountInactive) as error:
            abort(403)
    return wrapper