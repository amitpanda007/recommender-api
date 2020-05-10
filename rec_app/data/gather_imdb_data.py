import sys
import csv

from rec_app.common.imdb_service import get_movie_obj, extract_movie_info

MOVIE_ID_START = 1
MOVIE_ID_SEED = '0000000'


def load_data_to_csv(write_header=True):
    global MOVIE_ID_START

    while True:
        if MOVIE_ID_START > 9900000:
            sys.exit(1)

        try:
            current_movie_id = MOVIE_ID_SEED[:-len(str(MOVIE_ID_START))]
            print(current_movie_id + str(MOVIE_ID_START))
            movie_obj = get_movie_obj(current_movie_id+str(MOVIE_ID_START))

            if movie_obj:
                imdb_id = extract_movie_info(movie_obj, "ID")
                type = extract_movie_info(movie_obj, "TYPE")
                title = extract_movie_info(movie_obj, "TITLE")
                imdb_url = "https://www.imdb.com/title/{}/".format('tt'+current_movie_id+str(MOVIE_ID_START))
                genre = extract_movie_info(movie_obj, "GENRE")
                cover_image = extract_movie_info(movie_obj, "IMAGE")
                year = extract_movie_info(movie_obj, "YEAR")
                imdb_votes = extract_movie_info(movie_obj, "VOTES")
                imdb_rating = extract_movie_info(movie_obj, "RATING")
                story_line = extract_movie_info(movie_obj, "STORY")
                movie = [imdb_id,type,title,imdb_url,genre,cover_image,year,imdb_votes,imdb_rating,story_line]

                # print(movie)

                with open("imdb_data_dump.csv", 'a', newline='') as file:
                    wr = csv.writer(file, quoting=csv.QUOTE_ALL)
                    if write_header:
                        write_header = False
                        header = ["imdb_id", "type", "title", "imdb_url", "genre", "cover_image", "year", "imdb_votes", "imdb_rating", "story_line"]
                        wr.writerow(header)
                    wr.writerow(movie)

            MOVIE_ID_START += 1

        except Exception as E:
            MOVIE_ID_START += 1


if __name__ == "__main__":
    load_data_to_csv()