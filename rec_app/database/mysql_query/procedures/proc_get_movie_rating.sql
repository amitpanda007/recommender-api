USE `recommend`;
DROP procedure IF EXISTS `getMovieRating`;

DELIMITER $$
USE `recommend`$$
CREATE DEFINER=`root`@`%` PROCEDURE `getMovieRating`(IN _id int(6))
BEGIN
		SELECT rating FROM user_ratings WHERE movie_id=_id;
END$$

DELIMITER ;