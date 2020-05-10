USE `recommend`;
DROP procedure IF EXISTS `getMovieInfo`;

DELIMITER $$
USE `recommend`$$
CREATE DEFINER=`root`@`%` PROCEDURE `getMovieInfo`(IN _id int(6))
BEGIN
    SELECT movie_title,genre,imdb_url,cover_image,story_line FROM movies WHERE movie_id=_id;
END$$

DELIMITER ;