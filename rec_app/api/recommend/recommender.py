import logging
import random
import traceback

from flask_restplus import Resource
from flask_jwt_extended import get_jwt_identity, jwt_required

from rec_app.api.restplus import api
from rec_app.api.recommend.logic.matrix_factorization import recommend_new_user
from rec_app.database import db
from rec_app.database.models.movie_model import MoviesModel
from rec_app.database.models.recommendations_model import RecommendationsModel, RecommendationsEnum
from rec_app.database.models.user_ratings_model import UserRatingsModel
from rec_app.task_queue.tasks.test_task import add_together

log = logging.getLogger(__name__)

# ns = Namespace('auth', description='Operations related to user authentication')
ns = api.namespace('recommend', description='Operations related to recommendation')


class RecEnum:
    ANO_USER_TYPE = "anonymous"
    REG_USER_TYPE = "registered"
    RTNG_SRC_DUMMY = "DUMMY"
    RTNG_SRC_WEB = "WEB"


@ns.route("/anonymous")
class DefaultRecommend(Resource):

    def get(self):
        user_id = random.randint(1, 800)
        print(user_id)
        movies_recommended = recommend_new_user(user_id, RecEnum.ANO_USER_TYPE)
        response = {"recommend": movies_recommended, "message": "Please find your recommendation"}
        return response


@ns.route("/movies")
class MoviesRecommend(Resource):

    @jwt_required
    def get(self):
        # TODO: What to recommend to the user should be decided by API based on user behaviour on site
        current_user = get_jwt_identity()
        user_id = current_user['user_id']

        # Check user recommendation available status [available status : AVAILABLE, EMPTY, PROCESSING]
        usr_rec = RecommendationsModel.query.filter_by(user_id=user_id,
                                                       rec_type=RecommendationsEnum.MATRIX_FACTORIZATION).first()
        if usr_rec.rec_avl_status == RecommendationsEnum.AVAILABLE_STATUS:
            print(RecommendationsEnum.AVAILABLE_STATUS)
            movies_recommended = []
            ids = usr_rec.rec_mov_ids
            movie_ids = ids.split(",")
            movie_titles = MoviesModel.query.filter(MoviesModel.movie_id.in_(movie_ids))

            for movie in movie_titles:
                movie_dict = {"movieName": movie.movie_title, "movieId": movie.movie_id}
                movies_recommended.append(movie_dict)

            response = {"recommend" : movies_recommended, "message": "Please find your recommendation"}
            return response

        elif usr_rec.rec_avl_status == RecommendationsEnum.EMPTY_STATUS:
            print(RecommendationsEnum.EMPTY_STATUS)
            usr_rec.rec_avl_status = RecommendationsEnum.PROCESSING_STATUS
            db.session.commit()
            try:
                movies_recommended = recommend_new_user(user_id, RecEnum.REG_USER_TYPE)
                movie_id_list = []
                for movie in movies_recommended:
                    movie_id_list.append(str(movie["movieId"]))
                usr_rec.rec_mov_ids = ",".join(movie_id_list)
                db.session.commit()
                usr_rec.rec_avl_status = RecommendationsEnum.AVAILABLE_STATUS
                db.session.commit()
                response = {"recommend": movies_recommended, "message": "Please find your recommendation"}
                return response
            except Exception as E:
                print(E)
                traceback.print_exc()
                usr_rec.rec_avl_status = RecommendationsEnum.EMPTY_STATUS
                db.session.commit()
                response = {"message": "We apologize. Something went wrong while looking for recommendation."}
                return response, 500

            return {"message": "We have started processing your request. It will be available in some time."}

        elif usr_rec.rec_avl_status == RecommendationsEnum.PROCESSING_STATUS:
            print(RecommendationsEnum.PROCESSING_STATUS)
            response = {"message": "We are still processing your request. Please check back after a while."}
            return response

        response = {"message": "We apologize. Something went wrong while looking for recommendation."}, 500
        return response


@ns.route("/genre")
class GenreRecommend(Resource):

    def get(self):
        add_together.delay(9999,235984398543)
        return "Done"