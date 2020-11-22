import logging
from flask_restplus import Resource
from flask_jwt_extended import get_jwt_identity, jwt_required
from rec_app.api.restplus import api
from rec_app.database.models.imdb_rating_model import ImdbUserRatingsModel

log = logging.getLogger(__name__)
ns = api.namespace('imdb_rating', description='Operations related to IMDB Movie Ratings')


@ns.route("/<movie_id>")
class ImdbRating(Resource):

    @jwt_required
    def get(self, movie_id):
        current_user = get_jwt_identity()
        if current_user.get('user_id') is not None:
            try:
                result = ImdbUserRatingsModel.query.filter_by(imdb_movie_id=movie_id).first()
                # results = ImdbUserRatingsModel.query.filter(ImdbUserRatingsModel.imdb_url_id.endswith('1000')).all()
                # for result in results:
                #     print(result.get_rating())
                ratings = result.get_rating()
                if result:
                    final_result = {"movieId": result.imdb_movie_id, "imdbUserRating": ratings}
                    return final_result
                else:
                    final_result = {"movieId": int(movie_id), "imdbUserRating": "", "message": "Rating information not found"}
                    return final_result
            except AttributeError:
                final_result = {"movieId": "", "userRating": "", "message": "Error occured gathering rating information"}
                return final_result
        else:
            return {"message": "User information not found"}