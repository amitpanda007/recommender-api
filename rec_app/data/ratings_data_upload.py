import datetime
import pandas as pd
import csv

from rec_app.database.db_connector import MySQLDatabaseConnector
from rec_app.common.imdb_service import extract_movie_url_genre


def format_unix_time(time):
    return datetime.datetime.utcfromtimestamp(int(time)).strftime('%Y-%m-%d %H:%M:%S')


def gather_data_from_csv():
    rating_columns = ['user_id', 'movie_id', 'rating', 'timestamp']
    rating_frame = pd.read_csv("u.data", sep='\t', names=rating_columns)
    movie_columns = ['movie_id', 'movie_title', 'release_date', 'video release date', 'IMDb URL', 'unknown', 'Action',
                     'Adventure', 'Animation', 'Childrens', 'Comedy', 'Crime', 'Documentary', 'Drama', 'Fantasy',
                     'Film-Noir', 'Horror', 'Musical', 'Mystery', 'Romance', 'Sci-Fi', 'Thriller', 'War', 'Western']
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
        # for index in range(0, 50):
        value = [user_id_list[index], movie_id_list[index], rating_list[index], format_unix_time(timestamp_list[index])]
        ratings_list.append(value)

    movies_list = []
    # for index in range(0, 10):
    for index in range(len(unique_movie_title_list)):
        print("From IMDB API Gathering data for Movie : {}".format(unique_movie_title_list[index]))
        imdb_url_genre = extract_movie_url_genre(unique_movie_title_list[index])
        value = [unique_movie_id_list[index], unique_movie_title_list[index], imdb_url_genre[0],
                 ",".join(imdb_url_genre[1])]
        movies_list.append(value)

    return ratings_list, movies_list


def load_data_to_csv():
    ratings_list, movies_list = gather_data_from_csv()
    with open("ratings_list_processed.csv", 'w', newline='') as file:
        header = ["user_id", "movie_id", "rating", "timestamp"]
        wr = csv.writer(file, quoting=csv.QUOTE_ALL)
        wr.writerow(header)
        for rating in ratings_list:
            wr.writerow(rating)

    with open("movies_list_processed.csv", 'w', newline='') as file:
        header = ["movie_id", "movie_title", "imdb_url", "genre", "timestamp"]
        wr = csv.writer(file, quoting=csv.QUOTE_ALL)
        wr.writerow(header)
        for movie in movies_list:
            wr.writerow(movie)


def gather_data_processed():
    movies_list = []
    with open("movies_list_processed.csv", newline='') as f1:
        movie_reader = csv.reader(f1, delimiter=',')
        for row in movie_reader:
            movies_list.append(row)

    ratings_list = []
    with open("ratings_list_processed.csv", newline='') as f2:
        rating_reader = csv.reader(f2, delimiter=',')
        for row in rating_reader:
            ratings_list.append(row)

    return ratings_list[1:], movies_list[1:]


def load_data_to_db():
    # ratings_list, movies_list = gather_data_from_csv()
    ratings_list, movies_list = gather_data_processed()
    db = MySQLDatabaseConnector()
    cursor = db.connect_db()

    for movie in movies_list:
        movie = [int(movie[0]), str(movie[1]), str(movie[2]), str(movie[3])]
        movie_insert_query = """INSERT INTO movies (movie_id, movie_title, imdb_url, genre, timestamp)
                               VALUES
                               ({}, "{}", "{}", "{}", "{}") """.format(movie[0], movie[1], movie[2], movie[3],
                                                                       datetime.datetime.utcnow())
        cursor.execute(movie_insert_query)
    db.get_connection().commit()

    for rating in ratings_list:
        rating = [int(rating[0]), str(rating[1]), str(rating[2]), str(rating[3])]
        rating_insert_query = """INSERT INTO user_ratings (user_id, movie_id, rating, timestamp)
                                       VALUES
                                       ({}, {}, {}, "{}") """.format(rating[0], rating[1], rating[2], rating[3])

        cursor.execute(rating_insert_query)
    db.get_connection().commit()
    db.close_db()


if __name__ == "__main__":
    load_data_to_db()
    # load_data_to_csv()
    # gather_data_processed()
