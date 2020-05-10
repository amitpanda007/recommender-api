import pandas as pd
import numpy as np
import os

from rec_app.api.recommend.logic.utilities import low_rank_matrix_factorization
from rec_app.database.db_connector import run_query

# Pandas Options to see rows & columns
pd.set_option('display.max_rows', 1000)
pd.set_option('display.max_columns', 10)
pd.set_option('display.max_colwidth', 10)


# Read data from local files & provide recommendation
def load_rating_movie_data_from_file():
    cur_path = os.path.dirname(__file__)
    movie_rating_file = os.path.abspath(os.path.join(cur_path, "..", "..", "..", "data\\movie_ratings_data_set.csv"))
    movie_file = os.path.abspath(os.path.join(cur_path, "..", "..", "..", "data\\movies.csv"))
    ratings_ds = pd.read_csv(movie_rating_file)  # Load user ratings
    movies_ds = pd.read_csv(movie_file) # Load movie titles
    return ratings_ds, movies_ds


def limited_load_rating_movie_data_from_db():
    limited_movies = (242,302,377,51,346,474,265,465,451,86,257,1014,222,40,29,785,387,274,1042,1184,392,486,144,118,1,
                      546,95,768,277,234,246,98,193,88,194,1081,603,796,32,16,304,979,564,327,201,1137,241,4,332,100)
    user_ratings_query = "SELECT USER_ID, MOVIE_ID, RATING FROM user_ratings WHERE movie_id in {} ORDER BY USER_ID;".format(limited_movies)
    movies_query = "SELECT MOVIE_ID, MOVIE_TITLE, GENRE FROM movies WHERE movie_id in {} ;".format(limited_movies)
    user_ratings = run_query(user_ratings_query, "fetch_all")
    movies = run_query(movies_query, "fetch_all")
    ratings_df = pd.DataFrame(user_ratings, columns=['user_id', 'movie_id', 'value'])
    ratings_df['movie_id'] = ratings_df['movie_id'].astype(float)
    ratings_df['value'] = ratings_df['value'].astype(float)
    movies_df = pd.DataFrame(movies, columns=['movie_id', 'title', 'genre'])
    movies_df['movie_id'] = movies_df['movie_id'].astype(float)
    return ratings_df, movies_df


def load_rating_movie_data_from_db():
    user_ratings_query = "SELECT USER_ID, MOVIE_ID, RATING FROM user_ratings ORDER BY USER_ID;"
    movies_query = "SELECT MOVIE_ID, MOVIE_TITLE, GENRE FROM movies;"
    user_ratings = run_query(user_ratings_query, "fetch_all")
    movies = run_query(movies_query, "fetch_all")
    ratings_df = pd.DataFrame(user_ratings, columns=['user_id', 'movie_id', 'value'])
    ratings_df['movie_id'] = ratings_df['movie_id'].astype(float)
    ratings_df['value'] = ratings_df['value'].astype(float)
    movies_df = pd.DataFrame(movies, columns=['movie_id', 'title', 'genre'])
    movies_df['movie_id'] = movies_df['movie_id'].astype(float)
    return ratings_df, movies_df


# TODO : Change the temp function with a better performing low rank calculation function
def low_rank_matrix(user_id, user_type):
    # ratings_ds_df, movies_ds_df = load_rating_movie_data_from_file()
    from rec_app.api.recommend import RecEnum
    if user_type == RecEnum.ANO_USER_TYPE:
        print(RecEnum.ANO_USER_TYPE)
        ratings_ds_df, movies_ds_df = limited_load_rating_movie_data_from_db()
    elif user_type == RecEnum.REG_USER_TYPE:
        print(RecEnum.REG_USER_TYPE)
        ratings_ds_df, movies_ds_df = load_rating_movie_data_from_db()

    # TODO Testing with this idea. need to update later
    temp_data = [user_id, 242.0, 1.0]
    ratings_ds_df = ratings_ds_df.append(pd.DataFrame([temp_data], columns=['user_id', 'movie_id', 'value']), ignore_index=True)

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
    return recommended_df["movie_id"].head(6).values.tolist(),recommended_df["title"].head(6).values.tolist()


def recommend_new_user(user_id, user_type):
    movies_to_recommend = low_rank_matrix(user_id, user_type)
    movies_id = movies_to_recommend[0]
    movies_title = movies_to_recommend[1]
    recommend_list = []
    for index in range(0,len(movies_id)):
        recommend_dict = {"movieName": movies_title[index], "movieId": int(movies_id[index])}
        recommend_list.append(recommend_dict)
    print(recommend_list)
    return recommend_list[1:]


if __name__ == "__main__":
    pass
    # from rec_app.api.recommend import RecEnum
    # print(recommend_new_user(945, RecEnum.REG_USER_TYPE))
    # load_rating_movie_data_from_db()