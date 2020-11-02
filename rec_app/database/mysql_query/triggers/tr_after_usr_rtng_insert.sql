DROP TRIGGER IF EXISTS tr_after_usr_rtng_insert;
DELIMITER //
CREATE TRIGGER tr_after_usr_rtng_insert AFTER INSERT
ON user_ratings
FOR EACH ROW
BEGIN
	DECLARE cur_votes INT;
    DECLARE mov_rating INT;
    DECLARE total_rating INT;
    DECLARE total_usr_rated INT;

	SET total_rating := (SELECT SUM(rating) FROM user_ratings WHERE movie_id=NEW.movie_id);
    SET total_usr_rated := (SELECT COUNT(rating) FROM user_ratings WHERE movie_id=NEW.movie_id);
    SET mov_rating := total_rating / total_usr_rated;

	UPDATE movies SET user_votes = total_usr_rated WHERE movie_id = NEW.movie_id;
    UPDATE movies SET user_rating = mov_rating WHERE movie_id = NEW.movie_id;
END //
DELIMITER ;