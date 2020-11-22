import os
import pandas as pd
import numpy as np
from sklearn.decomposition import TruncatedSVD

from rec_app.database.db_connector import run_query, FetchType

rating_columns = ['user_id', 'movie_id', 'rating', 'timestamp']


def load_rating_movie_data_from_file():
    cur_path = os.path.dirname(__file__)
    u_data_path = os.path.abspath(os.path.join(cur_path, "..", "..", "..", "data\\u.data"))
    m_item_path = os.path.abspath(os.path.join(cur_path, "..", "..", "..", "data\\u.item"))
    ratings_frame = pd.read_csv(u_data_path, sep='\t', names=rating_columns)
    movie_columns = ['movie_id', 'movie_title', 'release_date', 'video release date', 'IMDb URL', 'unknown', 'Action',
                     'Adventure', 'Animation', 'Childrens', 'Comedy', 'Crime', 'Documentary', 'Drama', 'Fantasy',
                     'Film-Noir',
                     'Horror', 'Musical', 'Mystery', 'Romance', 'Sci-Fi', 'Thriller', 'War', 'Western']
    movies_frame = pd.read_csv(m_item_path, sep='|', names=movie_columns, encoding='latin-1')
    return ratings_frame, movies_frame


def load_rating_movie_data_from_db():
    user_ratings_query = "SELECT USER_ID, MOVIE_ID, RATING FROM user_ratings ORDER BY USER_ID;"
    movies_query = "SELECT MOVIE_ID, MOVIE_TITLE, GENRE FROM movies;"
    user_ratings = run_query(user_ratings_query, FetchType.FETCH_ALL)
    movies = run_query(movies_query, FetchType.FETCH_ALL)
    ratings_df = pd.DataFrame(user_ratings, columns=['user_id', 'movie_id', 'rating'])
    movies_df = pd.DataFrame(movies, columns=['movie_id', 'movie_title', 'genre'])
    return ratings_df, movies_df


def svd_recommend(user_selected_movie):
    # ratings_frame, movies_frame = load_rating_movie_data_from_file()
    ratings_frame, movies_frame = load_rating_movie_data_from_db()
    movie_names = movies_frame[['movie_id', 'movie_title']]
    combined_movie_rating = pd.merge(ratings_frame, movie_names, on='movie_id')
    # combined_movie_rating_sorted = combined_movie_rating.groupby('movie_id')['rating'].count().sort_values(ascending=False)

    # Create a Pivot table of user vs movies with ratings
    ratings_crosstab = combined_movie_rating.pivot_table(values='rating', index='user_id', columns='movie_title', fill_value=0)
    # Get the values of pivot table and transpose the matrix to have all the movies ratings in one list
    X = ratings_crosstab.values.T
    # Create TruncatedSVD out of the matrix value
    SVD = TruncatedSVD(n_components=12, random_state=17)
    resultant_matrix = SVD.fit_transform(X)
    # Create correlation matrix to create list of characters of movies those co relate to other movies based on the resultant matrix created
    corr_matrix = np.corrcoef(resultant_matrix)

    # Get index of the movies and let the correlation index of movies similar
    movie_names = ratings_crosstab.columns
    movie_list = list(movie_names)

    try:
        user_selected_movie_index = movie_list.index(user_selected_movie)
    except ValueError:
        for index, movie_name in enumerate(movie_list):
            if user_selected_movie.lower() in movie_name.lower():
                user_selected_movie_index = index
                break

    corr_matrix_user_movie = corr_matrix[user_selected_movie_index]
    movie_recommend_on_source_movie = movie_names[(corr_matrix_user_movie < 1.0) & (corr_matrix_user_movie > 0.9)]

    final_recommend = []
    for movie_name in  movie_recommend_on_source_movie.to_list():
        recommend = {}
        mov_id = movies_frame[movies_frame["movie_title"] == movie_name]["movie_id"].values
        recommend["movieName"] = movie_name
        recommend["movieId"] = int(mov_id[0])
        final_recommend.append(recommend)

    return final_recommend


def recommend_top_5(source_movie: str):
    recommended_movies = svd_recommend(source_movie)
    return recommended_movies[:5]

print(recommend_top_5('Carmencita'))