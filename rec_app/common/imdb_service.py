from imdb import IMDb

ia = IMDb()


def extract_movie_url_genre(movie_name):
    movie_resp = ia.search_movie(movie_name)
    if movie_resp:
        movie = movie_resp[0]
        url = ia.get_imdbURL(movie)
        movie_obj = ia.get_movie(movie.movieID)
        genres = []
        if "genres" in movie_obj:
            for genre in movie_obj['genres']:
                genres.append(genre)
        return [url, genres]
    else:
        return ["",[""]]


if __name__ == "__main__":
    print(extract_movie_url_genre("Twelfth Night (1996)"))