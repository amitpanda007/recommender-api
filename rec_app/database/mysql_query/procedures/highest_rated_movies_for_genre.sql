USE `recommend`;
DROP procedure IF EXISTS `highest_rated_movies_for_genre`;

DELIMITER $$
USE `recommend`$$
CREATE PROCEDURE `highest_rated_movies_for_genre`(IN genre_name CHAR(15))
BEGIN
	SELECT A.movie_title FROM movies AS A
	JOIN user_ratings AS B
	ON A.movie_id = B.movie_id
	WHERE A.genre LIKE CONCAT('%', genre_name, '%')
	GROUP BY A.movie_title
	ORDER BY count(B.rating) DESC LIMIT 1;
END$$

DELIMITER ;