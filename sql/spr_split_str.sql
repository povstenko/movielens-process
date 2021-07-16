DROP PROCEDURE IF EXISTS spr_split_str;
CREATE PROCEDURE spr_split_str(
IN str NVARCHAR(255),
IN splitter NVARCHAR(255)
)
wholeblock:BEGIN
  DECLARE n INT DEFAULT 0;
  DECLARE i INT DEFAULT 0;
  SET i = 1;
  SET n = (CHAR_LENGTH(str) - CHAR_LENGTH(REPLACE(str, splitter, '')));
  DROP TEMPORARY TABLE IF EXISTS tmp_splitted_str;
  CREATE TEMPORARY TABLE tmp_splitted_str(str NVARCHAR(255));

  WHILE i <= n+1 DO
    INSERT INTO tmp_splitted_str SELECT SUBSTRING_INDEX(SUBSTRING_INDEX(str, splitter, i), splitter, -1);
    SET i = i + 1;
  END WHILE;
    SELECT * FROM tmp_splitted_str;
  -- DROP TABLE TempTable;
END;

CALL spr_split_str('Animation|Comedy|Adventure', '|');