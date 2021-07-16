DROP PROCEDURE IF EXISTS spr_split_str;
CREATE procedure test.spr_split_str(
IN str NVARCHAR(255),
IN splitter NVARCHAR(255)
)
wholeblock:BEGIN
  declare n INT default 0;
  declare x INT default 0;
  SET x = 1;
  SET n = (CHAR_LENGTH(str) - CHAR_LENGTH(REPLACE(str, splitter, '')));
  CREATE TEMPORARY TABLE TempTable(str NVARCHAR(255));

  WHILE x <= n+1 DO
    INSERT INTO TempTable SELECT SUBSTRING_INDEX(SUBSTRING_INDEX(str, splitter, x), splitter, -1);
    SET x = x + 1;
  END WHILE;
    SELECT * FROM TempTable;
  DROP TABLE TempTable;
END;

CALL spr_split_str('Animation|Comedy|Adventure', '|')