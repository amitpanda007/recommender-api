USE `recommend`;
DROP procedure IF EXISTS `getAllMovies`;

DELIMITER $$
USE `recommend`$$
CREATE DEFINER=`root`@`%` PROCEDURE `getAllMovies`(IN id_from int(6), IN id_to int(6))
BEGIN
		SELECT DISTINCT movie_title,imdb_url FROM movies WHERE id >= id_from AND id <= id_to;
END$$

DELIMITER ;