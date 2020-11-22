import csv
import threading
import time
from concurrent.futures.thread import ThreadPoolExecutor
from datetime import datetime, date
from random import random

import requests
from bs4 import BeautifulSoup
import re

from rec_app.data.db_data_upload import get_cursor
from rec_app.database.db_connector import run_query, FetchType


def gather_movie_ratings(mov_id):
    mov_rtg_url = 'https://www.imdb.com/title/{}/ratings'.format(mov_id)
    page = requests.get(mov_rtg_url)
    soup = BeautifulSoup(page.content, 'html.parser')
    tables = soup.find_all(name='table')
    if len(tables) > 0:
        rating_table = tables[0]
        rating_star = rating_table.find_all('div', class_='rightAligned')
        # rating_percentage = rating_table.find_all('div', class_='topAligned')
        rating_votes = rating_table.find_all('div', class_='leftAligned')

        # movie_rating = {}
        rating_lst = []
        for idx in range(1, 11):
            rating = (rating_star[idx].text, rating_votes[idx].text)
            rating_lst.append(rating)
        # movie_rating[mov_id] = rating_lst

        return rating_lst


def gather_movies_from_db():
    db, cursor = get_cursor()
    movies_count_query = """SELECT MAX(ID) FROM movies"""
    movies_count = run_query(movies_count_query, FetchType.FETCH_ONE)

    with open('movie_info.csv', 'a+', newline='') as file:
        for idx in range(1, movies_count):
            movies_info_query = """SELECT imdb_url FROM movies WHERE movie_id={}""".format(idx)
            try:
                movies_info = run_query(movies_info_query, FetchType.FETCH_ONE)
                m = re.search('title/(.+?)/', movies_info)
                if m:
                    imdb_url_id = m.group(1)
                info = "{},{}".format(idx,imdb_url_id)
                file.writelines(info)
            except:
                continue
    db.close_db()


def write_rating_to_csv(movie_id):
    imdb_base_id = "tt00000000"
    imdb_url_id = imdb_base_id[:-len(str(movie_id))] + str(movie_id)

    try:
        ratings_info = gather_movie_ratings(imdb_url_id)
        if ratings_info is not None:
            rating_value = [imdb_url_id, movie_id]
            for rating in ratings_info:
                rating_value.append(rating[1])
            with open("ratings_votes_{}.csv".format(threading.current_thread().getName().split("_")[1]), 'a+', newline='') as file:
                # header = ["imdb_url_id", "movie_id", "ten_star", "nine_star", "eight_star", "seven_star", "six_star",
                #           "five_star", "four_star", "three_star", "two_star", "one_star"]
                wr = csv.writer(file, quoting=csv.QUOTE_ALL)
                # wr.writerow(header)
                wr.writerow(rating_value)

            with open("rating_index.txt", 'w+') as fi:
                fi.write(str(movie_id))
                fi.close()

    except Exception as e:
        with open("rating_index.txt", 'w+') as fi:
            fi.write(str(movie_id))
            fi.close()


def write_data_to_db():
    db,  cursor = get_cursor()
    ratings_lst = []
    with open("ratings_vote_list_count.csv", newline='') as file:
        rating_data = csv.reader(file, delimiter=',')
        for row in rating_data:
            ratings = [int(x) for x in row.replace('"','').split(',')[1:]]
            ratings_lst.append(ratings)

    for rt in ratings_lst:
        timestamp = datetime.utcnow()
        rating_ins_qry = """INSERT INTO imdb_user_ratings (movie_id, ten_star, nine_star, eight_star, seven_star, 
                            six_star, five_star, four_star, three_star, two_star, one_star, timestamp)
                            VALUES({}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}) """.format(
                            rt[0],rt[1],rt[2],rt[3],rt[4],rt[5],rt[6],rt[7],rt[8],rt[9],rt[10],rt[11],timestamp)

        cursor.execute(rating_ins_qry)
    db.get_connection().commit()


if __name__ == "__main__":
    MAX_NUMBER = 13399850
    # tt13399850
    # ID = 'tt1825683' full rating
    # ID = 'tt0000217' no rating info
    # ID = 'tt0000219' zero rating for some

    # print(gather_movie_ratings('tt1825683'))
    with open('rating_index.txt', 'r') as f:
        imdb_cur_idx = int(f.readlines()[0])
        f.close()

    run_list = [x for x in range(imdb_cur_idx, MAX_NUMBER, 100000)]
    for index, run in enumerate(run_list):
        try:
            if index + 1 < len(run_list):
                with ThreadPoolExecutor(max_workers=2) as executor:
                    executor.map(write_rating_to_csv, range(run_list[index], run_list[index + 1]))
        except:
            with open("ERROR_DUMP_{}.txt".format(date.today()), 'a') as file:
                file.writelines(str(run))
                file.writelines(",")

