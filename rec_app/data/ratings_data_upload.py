import datetime
import pandas as pd

from rec_app.database.db_connector import MySQLDatabaseConnector
from rec_app.common.imdb_service import extract_movie_url_genre


def format_unix_time(time):
    return datetime.datetime.utcfromtimestamp(int(time)).strftime('%Y-%m-%d %H:%M:%S')


rating_columns = ['user_id', 'movie_id', 'rating', 'timestamp']
rating_frame = pd.read_csv("u.data", sep='\t', names=rating_columns)
movie_columns = ['movie_id', 'movie_title', 'release_date', 'video release date', 'IMDb URL', 'unknown', 'Action',
                 'Adventure', 'Animation', 'Childrens', 'Comedy', 'Crime', 'Documentary', 'Drama', 'Fantasy',
                 'Film-Noir',
                 'Horror', 'Musical', 'Mystery', 'Romance', 'Sci-Fi', 'Thriller', 'War', 'Western']
movies_frame = pd.read_csv("u.item", sep='|', names=movie_columns, encoding='latin-1')
movie_names = movies_frame[['movie_id', 'movie_title']]
all_movie_rating_df = pd.merge(rating_frame, movie_names, on='movie_id')
all_movies_df = all_movie_rating_df.drop_duplicates(subset="movie_id")
# print(all_movie_rating.head())

user_id_list = all_movie_rating_df["user_id"].tolist()
movie_id_list = all_movie_rating_df["movie_id"].tolist()
rating_list = all_movie_rating_df["rating"].tolist()
timestamp_list = all_movie_rating_df["timestamp"].tolist()
movie_title_list = all_movie_rating_df["movie_title"].tolist()

unique_movie_id_list = all_movies_df["movie_id"].tolist()
unique_movie_title_list = all_movies_df["movie_title"].tolist()

ratings_list = []
for index in range(0, len(user_id_list)):
# for index in range(0, 1000):
    value = [user_id_list[index], movie_id_list[index], rating_list[index], format_unix_time(timestamp_list[index])]
    ratings_list.append(value)

movies_list = []
for index in range(len(unique_movie_title_list)):
# for index in range(0, 10):
    print("From IMDB API Gathering data for Movie : {}".format(unique_movie_title_list[index]))
    imdb_url_genre = extract_movie_url_genre(unique_movie_title_list[index])
    value = [unique_movie_id_list[index], unique_movie_title_list[index], imdb_url_genre[0], ",".join(imdb_url_genre[1])]
    movies_list.append(value)


db = MySQLDatabaseConnector()
cursor = db.connect_db()

for movie in movies_list:
    movie_insert_query = """INSERT INTO movies (movie_id, movie_title, imdb_url, genre, timestamp)
                           VALUES
                           ({}, "{}", "{}", "{}", "{}") """.format(movie[0], movie[1], movie[2], movie[3],
                                                                   datetime.datetime.utcnow())
    cursor.execute(movie_insert_query)
    db.get_connection().commit()

for rating in ratings_list:
    rating_insert_query = """INSERT INTO user_ratings (user_id, movie_id, rating, timestamp)
                                   VALUES
                                   ({}, {}, {}, "{}") """.format(rating[0], rating[1], rating[2], rating[3])

    cursor.execute(rating_insert_query)
    db.get_connection().commit()
db.close_db()

if __name__ == "__main__":
    pass
