import sys
from concurrent.futures.thread import ThreadPoolExecutor
from datetime import date
import csv
import threading

from rec_app.common.imdb_service import get_movie_obj, extract_movie_info

global_lock = threading.Lock()

MOVIE_ID_START = 1
MOVIE_ID_SEED = '00000000'


def load_data_to_csv(movie_id):
    if movie_id > 13259998:
        sys.exit(1)

    #    if "MainThread" not in threading.current_thread().getName() and os.path.exists("imdb_data_dump_{}.csv".format(
    #    threading.current_thread().getName().split("_")[1])):
    #
    #        with open("imdb_data_dump_{}.csv".format(threading.current_thread().getName().split("_")[1]), 'a+',
    #                  newline='') as file:
    #            wr = csv.writer(file, quoting=csv.QUOTE_ALL)
    #            header = ["imdb_id", "type", "title", "imdb_url", "genre", "cover_image", "year", "imdb_votes",
    #                      "imdb_rating", "story_line"]
    #            wr.writerow(header)

    print(threading.current_thread().getName(), movie_id)

    try:
        current_movie_id = MOVIE_ID_SEED[:-len(str(movie_id))]
        print(current_movie_id + str(movie_id))
        movie_obj = get_movie_obj(current_movie_id + str(movie_id))

        if movie_obj:
            imdb_id = extract_movie_info(movie_obj, "ID")
            type = extract_movie_info(movie_obj, "TYPE")
            title = extract_movie_info(movie_obj, "TITLE")
            imdb_url = "https://www.imdb.com/title/{}/".format('tt' + current_movie_id + str(movie_id))
            genre = extract_movie_info(movie_obj, "GENRE")
            cover_image = extract_movie_info(movie_obj, "IMAGE")
            year = extract_movie_info(movie_obj, "YEAR")
            imdb_votes = extract_movie_info(movie_obj, "VOTES")
            imdb_rating = extract_movie_info(movie_obj, "RATING")
            story_line = extract_movie_info(movie_obj, "STORY")
            movie = [imdb_id, type, title, imdb_url, genre, cover_image, year, imdb_votes, imdb_rating, story_line]

            # print(movie)
            with open("imdb_data_dump_{}.csv".format(threading.current_thread().getName().split("_")[1]), 'a+',
                      newline='') as file:
                wr = csv.writer(file, quoting=csv.QUOTE_ALL)
                wr.writerow(movie)

            with open("imdb_idx.txt", 'w+') as fi:
                fi.write(str(movie_id))
                fi.close()

    except Exception as E:
        with open("imdb_idx.txt", 'w+') as fi:
            fi.write(str(movie_id))
            fi.close()


if __name__ == "__main__":
    with open('imdb_idx.txt', 'r') as f:
        imdb_cur_idx = int(f.readlines()[0])
        f.close()

    run_list = [imdb_cur_idx - (x * 100000) for x in range(round(imdb_cur_idx / 100000))]

    for index, run in enumerate(run_list):
        try:
            if index + 1 < len(run_list):
                with ThreadPoolExecutor(max_workers=3) as executor:
                    executor.map(load_data_to_csv, reversed(range(run_list[index + 1], run_list[index] + 1)))
        except:
            with open("ERROR_DUMP_{}.txt".format(date.today()), 'a') as file:
                file.writelines(str(run))
                file.writelines(",")