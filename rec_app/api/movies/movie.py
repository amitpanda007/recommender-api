import logging
import traceback

from flask_restplus import Resource

from rec_app.api.restplus import api
from rec_app.common.imdb_service import extract_movie_image_url, extract_movie_story_line
from rec_app.database import db
from rec_app.database.db_connector import run_procedure, update_db
from rec_app.database.models.movie_model import MoviesModel
from rec_app.database.models.user_ratings_model import UserRatingsModel

log = logging.getLogger(__name__)

ns = api.namespace('movie', description='Operations related to getting all movie list')


@ns.route("/<movie_id>")
class Movies(Resource):
    """
    # Returns genre, imdb_url, storyline, image, average_rating
    """

    def get(self, movie_id):
        # Gather information for a movie : movie_title,genre,imdb_url,cover_image,story_line
        # prc_args = (movie_id,)
        # movie_info = run_procedure("getMovieInfo", prc_args, "fetch_one")
        movie_info = MoviesModel.query.filter_by(movie_id=movie_id).first()

        movie_name = movie_info.movie_title
        genre = movie_info.genre
        imdb_url = movie_info.imdb_url
        release_year = movie_info.release_year
        cover_image = movie_info.cover_image
        imdb_votes = movie_info.imdb_votes
        imdb_rating = movie_info.imdb_rating
        user_rating = movie_info.user_rating
        story_line = movie_info.story_line

        if cover_image is None:
            # Call IMDB API to get the cover image
            cover_image = extract_movie_image_url(movie_info.movie_title)
            # Update database with the gathered data
            try:
                movie_info.cover_image = cover_image
                db.session.commit()
            except:
                traceback.print_stack()
                return {"message": "Something went wrong"}, 500
        if story_line is None:
            # Call IMDB API to get the story line of the movie
            story_line = extract_movie_story_line(movie_info.movie_title)
            story_line = (story_line[:997] + '..') if len(story_line) > 999 else story_line
            # Update database with the gathered data
            try:
                movie_info.story_line = story_line
                db.session.commit()
            except:
                traceback.print_stack()
                return {"message": "Something went wrong"}, 500

        # Experimental Code for removing resolution information from image url
        if cover_image is not "":
            cover_image_new = cover_image.split("_V1")
            cover_image = cover_image_new[0] + "_V1"

        if user_rating is not None:
            user_rating = int(user_rating) * 2

        movie = {"movieName": movie_name, "genre": genre, "imdbUrl": imdb_url, "coverImage": cover_image,
                 "storyLine": story_line, "imdbRating": imdb_rating, "userRating": user_rating,
                 "releaseYear": release_year, "imdbVotes": imdb_votes}

        return movie
