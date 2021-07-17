DROP PROCEDURE IF EXISTS spr_split_str;
DELIMITER $$
CREATE PROCEDURE spr_split_str(
    IN str VARCHAR(255),
    IN splitter VARCHAR(255)
)
wholeblock:BEGIN
    DECLARE n INT DEFAULT 0;
    DECLARE i INT DEFAULT 0;
    SET i = 1;
    SET n = (CHAR_LENGTH(str) - CHAR_LENGTH(REPLACE(str, splitter, '')));
    DROP TEMPORARY TABLE IF EXISTS tmp_splitted_str;
    CREATE TEMPORARY TABLE tmp_splitted_str(str VARCHAR(255));

    WHILE i <= n+1 DO
        INSERT INTO tmp_splitted_str
        SELECT SUBSTRING_INDEX(SUBSTRING_INDEX(str, splitter, i), splitter, -1);
        SET i = i + 1;
    END WHILE;
END $$

-- CALL spr_split_str('Animation|Comedy|Adventure', '|');