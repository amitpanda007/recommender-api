USE `recommend`;
DROP procedure IF EXISTS `highest_rated_movies_for_genre`;

DELIMITER $$
USE `recommend`$$
CREATE PROCEDURE `highest_rated_movies_for_genre`(IN genre_name CHAR(15))
BEGIN
	DECLARE top_movie_usr_rtn VARCHAR(500);
    DECLARE top_movie_imdb_rtn VARCHAR(500);

	SET top_movie_usr_rtn := (SELECT A.movie_title FROM movies AS A
	JOIN user_ratings AS B
	ON A.movie_id = B.movie_id
	WHERE A.genre LIKE CONCAT('%', genre_name, '%')
	GROUP BY A.movie_title
	ORDER BY count(B.rating) DESC LIMIT 1);

    IF (top_movie_usr_rtn IS null) THEN
		SET top_movie_imdb_rtn := (SELECT A.movie_title FROM movies AS A
		WHERE A.genre LIKE CONCAT('%', genre_name, '%')
		GROUP BY A.imdb_votes
		ORDER BY A.imdb_votes DESC LIMIT 1);
        SELECT top_movie_imdb_rtn;
	ELSE
		SELECT top_movie_usr_rtn;
    END IF;
END$$

DELIMITER ;