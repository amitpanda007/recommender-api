import pandas as pd
import numpy as np
import os

from rec_app.api.recommend.logic.utilities import low_rank_matrix_factorization
from rec_app.database.db_connector import run_query


# Read data from local files & provide recommendation
def load_rating_movie_data_from_file():
    cur_path = os.path.dirname(__file__)
    movie_rating_file = os.path.abspath(os.path.join(cur_path, "..", "..", "..", "data\\movie_ratings_data_set.csv"))
    movie_file = os.path.abspath(os.path.join(cur_path, "..", "..", "..", "data\\movies.csv"))
    ratings_ds = pd.read_csv(movie_rating_file)  # Load user ratings
    movies_ds = pd.read_csv(movie_file) # Load movie titles
    return ratings_ds, movies_ds


def load_rating_movie_data_from_db():
    user_ratings_query = "SELECT USER_ID, MOVIE_ID, RATING FROM user_ratings ORDER BY USER_ID;"
    movies_query = "SELECT MOVIE_ID, MOVIE_TITLE, GENRE FROM movies;"
    user_ratings = run_query(user_ratings_query)
    movies = run_query(movies_query)
    ratings_df = pd.DataFrame(user_ratings, columns=['user_id', 'movie_id', 'value'])
    ratings_df['movie_id'] = ratings_df['movie_id'].astype(float)
    ratings_df['value'] = ratings_df['value'].astype(float)
    movies_df = pd.DataFrame(movies, columns=['movie_id', 'title', 'genre'])
    movies_df['movie_id'] = movies_df['movie_id'].astype(float)
    return ratings_df, movies_df


def low_rank_matrix(user_id):
    # ratings_ds_df, movies_ds_df = load_rating_movie_data_from_file()
    ratings_ds_df, movies_ds_df = load_rating_movie_data_from_db()
    ratings_df = pd.pivot_table(ratings_ds_df, index='user_id', columns='movie_id', aggfunc=np.max)  # Convert the running list of user ratings into a matrix
    U, M = low_rank_matrix_factorization(ratings_df.values, num_features=15, regularization_amount=0.1)  # Apply matrix factorization to find the latent features
    predicted_ratings = np.matmul(U, M)  # Find all predicted ratings by multiplying U and M matrices

    reviewed_movies_df = ratings_ds_df[ratings_ds_df['user_id'] == user_id]
    reviewed_movies_df = reviewed_movies_df.merge(movies_ds_df, on='movie_id')

    user_ratings = predicted_ratings[user_id - 1]
    movies_ds_df['rating'] = user_ratings

    already_reviewed = reviewed_movies_df['movie_id']
    recommended_df = movies_ds_df[movies_ds_df.index.isin(already_reviewed) == False]
    recommended_df = recommended_df.sort_values(by=['rating'], ascending=False)
    return recommended_df[["title"]].head(6).values.tolist()


def recommend_new_user(user_id):
    movies_to_recommend = low_rank_matrix(user_id)
    return movies_to_recommend[1:]


# print(recommend_new_user(13))
# load_rating_movie_data_from_db()