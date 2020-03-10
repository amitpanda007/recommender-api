import logging

from flask import request
from flask_restplus import Resource
from flask_jwt_extended import get_jwt_identity, jwt_required

from rec_app.api.restplus import api
from rec_app.database.models.user_ratings_model import UserRatings

log = logging.getLogger(__name__)

ns = api.namespace('rating', description='Operations related to Movie Ratings')


@ns.route("/<movie_id>")
class Rating(Resource):

    @jwt_required
    def get(self, movie_id):
        current_user = get_jwt_identity()
        if current_user['user_id'] is not None:
            result = UserRatings.query.filter_by(item_id=movie_id).filter_by(user_id=current_user['user_id']).first()
            # result = UserRatings.query.filter_by(item_id=movie_id).filter_by(user_id=196).first()
            if result:
                final_result = {"movie_title": result.movie_title, "user_rating": result.rating}
                return final_result
            else:
                {"message": "User information not found"}
        else:
            return {"message": "User information not found"}

    @jwt_required
    def post(self, movie_id):
        current_user = get_jwt_identity()
        if current_user['user_id'] is not None:
            request_data = request.get_json()
            UserRatings.add_rating(current_user['user_id'], movie_id, request_data["rating"])
            return {"message": "Rated Successfully"}
        else:
            return {"message": "User information not found"}