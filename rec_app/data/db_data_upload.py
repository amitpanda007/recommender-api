import datetime
import pandas as pd
import csv
import re
import time

from rec_app.database.db_connector import MySQLDatabaseConnector
from rec_app.common.imdb_service import extract_movie_url_genre

MOVIE = "movie"
RATING = "rating"
USER = "user"
IMDB_RATING = "imdb_rating"
RATING_SOURCE = "IMPORT"


def format_unix_time(time):
    return datetime.datetime.utcfromtimestamp(int(time)).strftime('%Y-%m-%d %H:%M:%S')


def gather_data_from_csv():
    rating_columns = ['user_id', 'movie_id', 'rating', 'timestamp']
    rating_frame = pd.read_csv("movies_data/u.data", sep='\t', names=rating_columns)
    movie_columns = ['movie_id', 'movie_title', 'release_date', 'video release date', 'IMDb URL', 'unknown', 'Action',
                     'Adventure', 'Animation', 'Childrens', 'Comedy', 'Crime', 'Documentary', 'Drama', 'Fantasy',
                     'Film-Noir', 'Horror', 'Musical', 'Mystery', 'Romance', 'Sci-Fi', 'Thriller', 'War', 'Western']
    movies_frame = pd.read_csv("movies_data/u.item", sep='|', names=movie_columns, encoding='latin-1')
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
    with open("movies_data/ratings_list_processed.csv", 'w', newline='') as file:
        header = ["user_id", "movie_id", "rating", "timestamp"]
        wr = csv.writer(file, quoting=csv.QUOTE_ALL)
        wr.writerow(header)
        for rating in ratings_list:
            wr.writerow(rating)

    with open("movies_data/movies_list_processed.csv", 'w', newline='') as file:
        header = ["movie_id", "movie_title", "imdb_url", "genre", "timestamp"]
        wr = csv.writer(file, quoting=csv.QUOTE_ALL)
        wr.writerow(header)
        for movie in movies_list:
            wr.writerow(movie)


def gather_data_processed(data_type=None, file_path=None):
    movies_list = []
    ratings_list = []
    if data_type == MOVIE:
        path = "movies_list_processed.csv" if file_path is None else file_path
        with open(path, newline='', encoding='latin-1') as f1:
            movie_reader = csv.reader(f1, delimiter=',')
            for row in movie_reader:
                movies_list.append(row)
        return movies_list[1:]

    elif data_type == RATING:
        path = "ratings_list_processed.csv" if file_path is None else file_path
        with open(path, newline='', encoding='utf-8') as f2:
            rating_reader = csv.reader(f2, delimiter=',')
            for row in rating_reader:
                ratings_list.append(row)
        return ratings_list[1:]

    elif data_type == IMDB_RATING:
        path = "ratings_list_processed.csv" if file_path is None else file_path
        with open(path, newline='', encoding='utf-8') as f3:
            rating_reader = csv.reader(f3, delimiter=',')
            for row in rating_reader:
                ratings_list.append(row)
        return ratings_list[1:]


def load_user_from_db():
    user_list = []
    user_query = """SELECT DISTINCT user_id FROM user_ratings ORDER BY user_id"""
    db, cursor = get_cursor()
    cursor.execute(user_query)
    users = cursor.fetchall()
    for user in users:
        user_list.append(user[0])
    return user_list


def load_data_to_db(load_type=None, file_path=None):
    # ratings_list, movies_list = gather_data_from_csv()
    db, cursor = get_cursor()

    if load_type == MOVIE:
        index = 1
        start_time = time.time()
        movies_list = gather_data_processed(data_type=load_type, file_path=file_path)
        for movie in movies_list:
            print("Current running Index: {}".format(index))
            movie_id = int(movie[0])
            movie_title = str(movie[1]).replace('"','')
            imdb_url = str(movie[2])
            genre = str(movie[3])
            cover_image = 'Null' if str(movie[4]) == "0" else str(movie[4])
            release_year = int(float(movie[5]))
            imdb_votes = int(float(movie[6]))
            imdb_rating = int(float(movie[7]))
            user_rating = 'Null'
            user_votes = 'Null'
            story_line = 'Null' if str(movie[8]) == "0" else str(movie[8])
            timestamp = datetime.datetime.utcnow()

            if "[" in genre:
                genre = re.sub(r'\[|\]|\"|\'| ', "", genre)

            if "[" in story_line or "]" in story_line or '"' in story_line:
                story_line = re.sub(r'\[|\]|\"', "", story_line)

            if story_line != 'Null':
                story_line= '"{}"'.format(story_line)

            if cover_image != 'Null':
                cover_image = '"{}"'.format(cover_image)

            movie_insert_query = """INSERT INTO movies (movie_id, movie_title, release_year, imdb_url, imdb_rating, 
                                    imdb_votes, user_rating, user_votes, genre, cover_image, story_line, timestamp)
                                   VALUES ({}, "{}", {}, "{}", {}, {}, {}, {}, "{}", {}, {}, "{}") """.format(movie_id,
                                    movie_title, release_year, imdb_url, imdb_rating, imdb_votes, user_rating,
                                    user_votes, genre, cover_image, story_line, timestamp)

            # print(movie_insert_query)
            cursor.execute(movie_insert_query)
            index += 1
        db.get_connection().commit()
        end_time = time.time()
        print("Total time taken: {} mins".format(round((end_time - start_time)/60, 2)))

    if load_type == RATING:
        ratings_list = gather_data_processed(data_type=load_type, file_path=file_path)

        for rating in ratings_list:
            rating_data = [int(rating[0]), str(rating[1]), str(rating[2]), str(rating[3])]
            rating_insert_query = """INSERT INTO user_ratings (user_id, movie_id, rating, rating_source, timestamp)
                                    VALUES({}, {}, {}, "{}", "{}") """.format(rating_data[0], rating_data[1],
                                                                        rating_data[2], RATING_SOURCE, rating_data[3])
            cursor.execute(rating_insert_query)
        db.get_connection().commit()

    if load_type == IMDB_RATING:
        index = 1
        start_time = time.time()
        imdb_ratings_list = gather_data_processed(data_type=load_type, file_path=file_path)
        timestamp = datetime.datetime.utcnow()
        for rating in imdb_ratings_list:
            print("Current running Index: {}".format(index))
            rating_insert_query = """INSERT INTO imdb_user_ratings (imdb_url_id, imdb_movie_id, ten_rtn_cnt, 
                                nine_rtn_cnt, eight_rtn_cnt, seven_rtn_cnt, six_rtn_cnt, five_rtn_cnt , four_rtn_cnt,
                                three_rtn_cnt, two_rtn_cnt, one_rtn_cnt, rating_source, timestamp)
                                VALUES("{}", {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, "{}", "{}") """.format(
                                rating[0], int(rating[1]), int(rating[2]), int(rating[3]), int(rating[4]),
                                int(rating[5]), int(rating[6]), int(rating[7]), int(rating[8]), int(rating[9]),
                                int(rating[10]), int(rating[11]), RATING_SOURCE, timestamp)
            cursor.execute(rating_insert_query)
            index += 1
        db.get_connection().commit()
        end_time = time.time()
        print("Total time taken: {} mins".format(round((end_time - start_time) / 60, 2)))

    if load_type == USER:
        users_list = load_user_from_db()
        index = 0
        first_name = "Test{}"
        last_name = "UserModel"
        username = "testuser{}"
        email = "testuser{}@test.com"
        password_hash = "password"
        preferred_genres = "Null"
        initial_setup = False
        for user in users_list:
            user_insert_query = """INSERT INTO users (user_id, first_name, last_name, username, email, password_hash, 
                                    preferred_genres, initial_setup) VALUES({}, "{}", "{}", "{}", "{}", "{}", {}, 
                                    {}) """.format(user, first_name.format(index), last_name, username.format(index),
                                    email.format(index), password_hash, preferred_genres, initial_setup)

            cursor.execute(user_insert_query)
            index += 1
        db.get_connection().commit()

    db.close_db()


def get_cursor():
    db = MySQLDatabaseConnector()
    cursor = db.connect_db()
    return db, cursor


if __name__ == "__main__":
    # load_data_to_db(load_type=MOVIE, file_path="F:\\CODING\\PYTHON\\IMDB_Data_Load\\dump\\movies\\processed_movie.csv")
    # load_data_to_db(load_type=IMDB_RATING,
    #                 file_path="F:\\CODING\\PYTHON\\IMDB_Data_Load\\dump\\ratings\\processed_ratings_final.csv")
    # load_data_to_csv()
    # gather_data_processed()
    pass