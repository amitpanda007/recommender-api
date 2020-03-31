import logging
from flask import request
from flask_restplus import Resource

from rec_app.api.restplus import api
from rec_app.database.db_connector import MySQLDatabaseConnector
from rec_app.database.models.movie_model import Movie

log = logging.getLogger(__name__)

ns = api.namespace('movies', description='Operations related to getting all movie list')


@ns.route("/all")
class Movies(Resource):

    def get(self):
        movie_seq_from = request.args.get("from")
        movie_seq_to = request.args.get("to")
        if movie_seq_from and movie_seq_to:
            proc_args = movie_seq_from, movie_seq_to
        else:
            proc_args = 0, 10
        db = MySQLDatabaseConnector()
        cursor = db.connect_db()
        cursor.callproc("getAllMovies", proc_args)

        final_list = []
        for result in cursor.stored_results():
            all_movies = result.fetchall()
            for movies in all_movies:
                movie_dict = {"movieName": movies[0], "imdbUrl": movies[1]}
                final_list.append(movie_dict)
        return final_list
