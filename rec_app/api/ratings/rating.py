import logging
import traceback

from flask import request
from flask_restplus import Resource
from flask_jwt_extended import get_jwt_identity, jwt_required

from rec_app.api.recommend import RecEnum
from rec_app.api.restplus import api
from rec_app.database.models.user_ratings_model import UserRatingsModel

log = logging.getLogger(__name__)
ns = api.namespace('rating', description='Operations related to Movie Ratings')

RATING_SOURCE_USER = "USER"


@ns.route("/<movie_id>")
class Rating(Resource):

    @jwt_required
    def get(self, movie_id):
        current_user = get_jwt_identity()
        if current_user.get('user_id') is not None:
            try:
                result = UserRatingsModel.query.filter_by(movie_id=movie_id).filter_by(
                    user_id=current_user.get('user_id')).first()
                # result = UserRatingsModel.query.filter_by(item_id=movie_id).filter_by(user_id=196).first()
                if result:
                    final_result = {"movieId": result.movie_id, "userRating": result.rating}
                    return final_result
                else:
                    final_result = {"movieId": int(movie_id), "userRating": "", "message": "Rating information not found"}
                    return final_result
            except AttributeError:
                final_result = {"movieId": "", "userRating": "", "message": "Error occured gathering rating information"}
                return final_result
        else:
            return {"message": "User information not found"}

    @jwt_required
    def post(self, movie_id):
        current_user = get_jwt_identity()
        if current_user['user_id'] is not None:
            request_data = request.get_json()
            user_id = current_user['user_id']
            rating = request_data["rating"]
            print('USER_ID:',user_id,',','RATING:',rating)
            try:
                UserRatingsModel.add_rating(user_id, movie_id, rating, RATING_SOURCE_USER)
                UserRatingsModel.query.filter_by(user_id=user_id, rating_source=RecEnum.RTNG_SRC_DUMMY).delete()
                return {"message": "Rated Successfully"}
            except Exception as E:
                traceback.print_exc()
                return {"message": "Something went wrong"}, 500
        else:
            return {"message": "User information not found"}
