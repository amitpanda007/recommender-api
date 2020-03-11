import pandas as pd
import numpy as np

from rec_app.api.recommend.utilities import low_rank_matrix_factorization


def low_rank_matrix(user_id):
    raw_dataset_df = pd.read_csv("movie_ratings_data_set.csv")  # Load user ratings
    movies_df = pd.read_csv("movies.csv")  # Load movie titles
    ratings_df = pd.pivot_table(raw_dataset_df, index='user_id', columns='movie_id', aggfunc=np.max)  # Convert the running list of user ratings into a matrix
    U, M = low_rank_matrix_factorization(ratings_df.values, num_features=15, regularization_amount=0.1)  # Apply matrix factorization to find the latent features
    predicted_ratings = np.matmul(U, M)  # Find all predicted ratings by multiplying U and M matrices

    reviewed_movies_df = raw_dataset_df[raw_dataset_df['user_id'] == user_id]
    reviewed_movies_df = reviewed_movies_df.merge(movies_df, on='movie_id')

    user_ratings = predicted_ratings[user_id - 1]
    movies_df['rating'] = user_ratings

    already_reviewed = reviewed_movies_df['movie_id']
    recommended_df = movies_df[movies_df.index.isin(already_reviewed) == False]
    recommended_df = recommended_df.sort_values(by=['rating'], ascending=False)
    return recommended_df[["title"]].head(6)


def recommend_new_user(user_id):
    movies_to_recommend = low_rank_matrix(user_id)
    return movies_to_recommend[1:]


print(recommend_new_user(8))
