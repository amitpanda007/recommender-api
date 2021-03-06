import os
import logging

from flask import request, jsonify
from flask_restplus import Resource

from rec_app import sqlfile_path
from rec_app.api.restplus import api
from rec_app.database.db_connector import run_query, run_procedure, FetchType

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
            proc_args = 1, 25
        all_movies = run_procedure("getMoviesSortedByYear", proc_args, FetchType.FETCH_ALL)

        # offset = int(movie_seq_from) - 1
        # limit = (int(movie_seq_to) - int(movie_seq_from)) + 1
        # movie_query = """SELECT DISTINCT movie_title,movie_id,release_year FROM movies ORDER BY
        #                 release_year DESC LIMIT {offset},{limit}""".format(offset=offset, limit=limit)
        # all_movies = run_query(movie_query, fetch_type=FetchType.FETCH_ALL)

        final_list = []
        for movies in all_movies:
            movie_dict = {"movieName": movies[0], "movieId": movies[1]}
            final_list.append(movie_dict)
        return final_list


@ns.route("/search/<movie_name>")
class Movies(Resource):

    def get(self, movie_name):
        search_query = "SELECT movie_title FROM movies WHERE movie_title LIKE '%{}%' LIMIT 10".format(movie_name)
        search_result = run_query(search_query, fetch_type=FetchType.FETCH_ALL)
        final_list = []
        for movies in search_result:
            final_list.append(movies[0])
        return final_list


@ns.route("/count")
class MoviesCount(Resource):
    def get(self):
        cur_path = os.path.dirname(__file__)
        sql_file = os.path.abspath(os.path.join(cur_path, "..", "..", sqlfile_path.MOVIES_COUNT))
        for line in open(sql_file):
            result = run_query(line, FetchType.FETCH_ONE)
            return {"totalMovies": result}


@ns.route("/genres")
class MovieGenres(Resource):

    def get(self):
        query = "SELECT genre FROM movies;"
        result = run_query(query, fetch_type=FetchType.FETCH_ALL)
        genre_list = []
        for genre in result:
            lst = genre[0].split(",")
            for gen in lst:
                if gen != '':
                    genre_list.append(gen)

        genres = list(set(genre_list))
        return {"genres": genres}