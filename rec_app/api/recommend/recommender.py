import logging

from flask import request
from flask_restplus import Resource

from rec_app.api.restplus import api
from rec_app.database.models.user_ratings_model import UserRatings
from .svd import svd_rec
from .matrix_factorization import recommend_new_user

log = logging.getLogger(__name__)

# ns = Namespace('auth', description='Operations related to user authentication')
ns = api.namespace('recommend', description='Operations related to SVD recommendation')


@ns.route("/default")
class DefaultRecommender(Resource):

    def post(self):
        user_info = request.get_json()
        movies = recommend_new_user(user_info["user_id"])
        return str(movies)


@ns.route("/svd")
class SvdRecommender(Resource):

    def get(self):
        movies = svd_rec("Star Wars (1977)")
        return str(movies)