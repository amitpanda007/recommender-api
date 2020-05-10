USE `recommend`;
DROP procedure IF EXISTS `getUserRatingCount`;

DELIMITER $$
USE `recommend`$$
CREATE DEFINER=`root`@`%` PROCEDURE `getUserRatingCount`(IN _id int(6))
BEGIN
		SELECT COUNT(rating) FROM user_ratings WHERE user_id=_id;
END$$

DELIMITER ;