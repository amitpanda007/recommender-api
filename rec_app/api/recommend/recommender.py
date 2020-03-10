import logging

from flask_restplus import Resource

from rec_app.api.restplus import api
from rec_app.database.models.user_ratings_model import UserRatings
from .svd_recommend import svd_rec

log = logging.getLogger(__name__)

# ns = Namespace('auth', description='Operations related to user authentication')
ns = api.namespace('recommend', description='Operations related to SVD recommendation')


@ns.route("/default")
class DefaultRecommender(Resource):

    def get(self):
        movies = svd_rec("Star Wars (1977)")
        return str(movies)


@ns.route("/svd")
class SvdRecommender(Resource):

    def get(self):
        movies = svd_rec("Star Wars (1977)")
        return str(movies)