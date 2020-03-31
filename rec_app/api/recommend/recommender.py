import logging

from flask import request
from flask_restplus import Resource

from rec_app.api.restplus import api
from rec_app.api.recommend.logic.svd import recommend_top_5
from rec_app.api.recommend.logic.matrix_factorization import recommend_new_user

log = logging.getLogger(__name__)

# ns = Namespace('auth', description='Operations related to user authentication')
ns = api.namespace('recommend', description='Operations related to SVD recommendation')


@ns.route("/default")
class DefaultRecommend(Resource):

    def post(self):
        user_info = request.get_json()
        movies = recommend_new_user(user_info["user_id"])
        movie_list = []
        for movie in movies:
            for mv in movie:
                movie_list.append(mv)
        return movie_list


@ns.route("/svd")
class SvdRecommend(Resource):

    def get(self):
        movies = recommend_top_5("Star Wars (1977)")
        return str(movies)