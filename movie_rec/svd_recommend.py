import pandas as pd
import numpy as np
from sklearn.decomposition import TruncatedSVD

rating_columns = ['user_id', 'item_id', 'rating', 'timestamp']
rating_frame = pd.read_csv('./movie_rec/u.data', sep='\t', names=rating_columns)

movie_columns = ['item_id', 'movie_title', 'release_date', 'video release date', 'IMDb URL', 'unknown', 'Action',
                 'Adventure', 'Animation', 'Childrens', 'Comedy', 'Crime', 'Documentary', 'Drama', 'Fantasy',
                 'Film-Noir',
                 'Horror', 'Musical', 'Mystery', 'Romance', 'Sci-Fi', 'Thriller', 'War', 'Western']
movies_frame = pd.read_csv('./movie_rec/u.item', sep='|', names=movie_columns, encoding='latin-1')
movie_names = movies_frame[['item_id', 'movie_title']]

combined_movie_rating = pd.merge(rating_frame, movie_names, on='item_id')

combined_movie_rating_sorted = combined_movie_rating.groupby('item_id')['rating'].count().sort_values(ascending=False)

# Create a Pivot table of user vs movies with ratings
ratings_crosstab = combined_movie_rating.pivot_table(values='rating', index='user_id', columns='movie_title',
                                                     fill_value=0)

# Get the values of pivot table and transpose the matrix to have all the movie ratings in one list
X = ratings_crosstab.values.T

# Create TruncatedSVD out of the matrix value
SVD = TruncatedSVD(n_components=12, random_state=17)
resultant_matrix = SVD.fit_transform(X)

# Create correlation matrix
corr_matrix = np.corrcoef(resultant_matrix)

# Get index of the movie and let the correlation index of movie similar
movie_names = ratings_crosstab.columns
movie_list = list(movie_names)


# TODO : change function to take input from user's movie choice
def top_n_movie(source_movie: str):
    star_wars = movie_list.index('Star Wars (1977)')
    corr_star_wars = corr_matrix[star_wars]
    movie_recommend_on_source_movie = movie_names[(corr_star_wars < 1.0) & (corr_star_wars > 0.9)]
    print(movie_recommend_on_source_movie)
    return movie_recommend_on_source_movie
