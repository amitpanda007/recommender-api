USE `recommend`;
DROP procedure IF EXISTS `getAllMovies`;

DELIMITER $$
USE `recommend`$$
CREATE PROCEDURE `getAllMovies`(IN id_from int(10), IN id_to int(10))
BEGIN
	DECLARE last_mov_idx INT;
    SET last_mov_idx := (SELECT MAX(id) FROM movies);
	SELECT DISTINCT movie_title,movie_id FROM movies WHERE id >= (last_mov_idx - id_to)  AND id <= (last_mov_idx - id_from);
END$$

DELIMITER ;