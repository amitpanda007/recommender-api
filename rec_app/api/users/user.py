import logging
import traceback

from flask import request
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restplus import Resource

from rec_app.api.recommend.recommender import RecEnum
from rec_app.api.restplus import api
from rec_app.database.models.movie_model import MoviesModel
from rec_app.database.models.user_model import UserModel
from rec_app.database.models.user_ratings_model import UserRatingsModel

log = logging.getLogger(__name__)

ns = api.namespace('user', description='Operations related to getting user information')


@ns.route("/info")
class UserInfo(Resource):
    """
    # Returns basic user information
    """

    @jwt_required
    def get(self):
        current_user = get_jwt_identity()
        user = UserModel.query.filter_by(user_id=current_user['user_id']).first()
        user_info = {"name": user.get_name(), "initialSetupDone": user.get_initial_setup_status()}
        return user_info


@ns.route("/update/<route>")
class UserInfo(Resource):

    @jwt_required
    def get(self, route):
        current_user = get_jwt_identity()
        user = UserModel.query.filter_by(user_id=current_user['user_id']).first()
        if route == "initial-setup":
            user.initial_setup = True
            user.update_user()
            return {"message": "Updated user Preference"}
        return {"message": "Unable to process request at the moment"}

    @jwt_required
    def post(self, route):
        current_user = get_jwt_identity()
        user_id = current_user['user_id']
        payload = request.json['data']
        print(payload)
        try:
            user = UserModel.query.filter_by(user_id=current_user['user_id']).first()
        except Exception as E:
            traceback.print_exc()
            return {"message": "Something went wrong"}, 500
        if route == "genre":
            user.preferred_genres = payload
            user.update_user()
            usr_rtng_dummy = UserRatingsModel.query.filter_by(user_id=user_id,
                                                              rating_source=RecEnum.RTNG_SRC_DUMMY).first()
            if usr_rtng_dummy is None:
                try:
                    random_movie = MoviesModel.get_random_movie()
                    UserRatingsModel.add_rating(user_id, random_movie.movie_id, 1, RecEnum.RTNG_SRC_DUMMY)
                except Exception as E:
                    traceback.print_exc()
                    return {"message": "Something went wrong"}, 500
            return {"message": "Updated user genre"}
        return {"message": "Unable to process request at the moment"}
