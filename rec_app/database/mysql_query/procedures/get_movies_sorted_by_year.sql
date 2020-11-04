USE `recommend`;
DROP procedure IF EXISTS `getMoviesSortedByYear`;

DELIMITER $$
USE `recommend`$$
CREATE PROCEDURE `getMoviesSortedByYear`(IN id_from int(10), IN id_to int(10))
BEGIN
	DECLARE offset_data INT;
    DECLARE limit_data INT;
    SET offset_data := id_from - 1;
    SET limit_data := (id_to - id_from) + 1;
	SELECT DISTINCT movie_title,movie_id,release_year FROM movies ORDER BY release_year DESC LIMIT offset_data,limit_data;
END$$

DELIMITER ;