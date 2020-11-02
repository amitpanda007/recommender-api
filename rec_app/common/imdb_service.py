import traceback

from imdb import IMDb, IMDbDataAccessError

ia = IMDb()


def movie_response(movie_name):
    movie_resp = ia.search_movie(movie_name)
    if movie_resp:
        movie = movie_resp[0]
        return movie


def extract_movie_url_genre(movie_name, _movie=None):
    if _movie is None:
        movie = movie_response(movie_name)
    if movie is not None:
        url = ia.get_imdbURL(movie)
        movie_obj = ia.get_movie(movie.movieID)
        genres = []
        if "genres" in movie_obj:
            for genre in movie_obj['genres']:
                genres.append(genre)
            return [url, genres]
        else:
            return ["",[""]]
    return ["",[""]]


def extract_movie_image_url(movie_name, _movie=None):
    print("Movie image not found in DB. Searching IMDB for image reference.")
    if _movie is None:
        movie = movie_response(movie_name)
    if movie is not None:
        movie_obj = ia.get_movie(movie.movieID)
        try:
            if movie_obj.has_key('cover url'):
                return movie_obj.get('cover url')
        except Exception as E:
            print(E)
            traceback.print_stack()
            return ""
    return ""


def extract_movie_story_line(movie_name, _movie=None):
    print("Story of Movie not found in DB. Searching IMDB for story information.")
    if _movie is None:
        movie = movie_response(movie_name)
    if movie is not None:
        movie_obj = ia.get_movie(movie.movieID)
        try:
            if movie_obj.has_key('plot outline'):
                return movie_obj.get('plot outline')
            elif movie_obj.has_key('plot'):
                return movie_obj.get('plot')
        except KeyError:
            # traceback.print_stack()
            return ""
    return ""


def get_movie_obj(movie_id):
    try:
        return ia.get_movie(movie_id)
    except (RuntimeError, Exception, IMDbDataAccessError):
        pass
        # print("Error occurred while searching for movie",movie_id)


def extract_movie_info(movie_obj, search_name):
    try:
        if search_name is "ID":
            if movie_obj.movieID:
                return movie_obj.movieID

        elif search_name is "TYPE":
            if movie_obj.has_key('kind'):
                return movie_obj.get('kind')

        elif search_name is "TITLE":
            if movie_obj.has_key('title'):
                return movie_obj.get('title')

        elif search_name is "URL":
            pass

        elif search_name is "GENRE":
            if movie_obj.has_key('genres'):
                return movie_obj.get('genres')

        elif search_name is "IMAGE":
            if movie_obj.has_key('cover url'):
                return movie_obj.get('cover url')

        elif search_name is "STORY":
            if movie_obj.has_key('plot outline'):
                return movie_obj.get('plot outline')
            elif movie_obj.has_key('plot'):
                return movie_obj.get('plot')

        elif search_name is "YEAR":
            if movie_obj.has_key('year'):
                return movie_obj.get('year')

        elif search_name is "VOTES":
            if movie_obj.has_key('votes'):
                return movie_obj.get('votes')

        elif search_name is "RATING":
            if movie_obj.has_key('rating'):
                return movie_obj.get('rating')

    except Exception as E:
        # print("Error occurred while searching for movie")
        pass


if __name__ == "__main__":
    pass
    # print(extract_movie_url_genre("Nosferatu a Venezia (1986)"))
    print(extract_movie_image_url("Joker (2019)"))
    # print(extract_movie_story_line("Right Stuff, The (1983)"))