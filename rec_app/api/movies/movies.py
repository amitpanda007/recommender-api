import logging
from flask_restplus import Resource

from rec_app.api.restplus import api
from rec_app.database.db_connector import MySQLDatabaseConnector
from rec_app.database.models.movie_model import Movie

log = logging.getLogger(__name__)

ns = api.namespace('movies', description='Operations related to SVD recommendation')


@ns.route("/all")
class Movies(Resource):

    def get(self):
        db = MySQLDatabaseConnector()
        cursor = db.connect_db()
        cursor.callproc("getAllMovies")
        final_list = []
        for result in cursor.stored_results():
            all_movies = result.fetchall()
            for movies in all_movies:
                for movie in movies:
                    final_list.append(movie)
        return final_list