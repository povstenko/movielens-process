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
        INSERT INTO tmp_splitted_str
        SELECT SUBSTRING_INDEX(SUBSTRING_INDEX(str, splitter, i), splitter, -1);
        SET i = i + 1;
    END WHILE;
END;

DROP PROCEDURE IF EXISTS spr_find_top_rated_movies;
CREATE PROCEDURE spr_find_top_rated_movies(
    IN n int,
    IN `regexp` varchar(200),
    IN year_from int,
    IN year_to int,
    IN genres varchar(255)
)
BEGIN
    DECLARE n_rows INT DEFAULT 0;
    DECLARE i INT DEFAULT 0;
    DECLARE genre NVARCHAR(100) DEFAULT 0;

    DROP TEMPORARY TABLE IF EXISTS tmp_result;
    CREATE TEMPORARY TABLE tmp_result(
        movieId INT,
        title NVARCHAR(255),
        genres NVARCHAR(255),
        year INT,
        rating FLOAT);

    CALL spr_split_str(genres, '|');

    SELECT COUNT(*) FROM tmp_splitted_str INTO n_rows;
    SET i = 0;

    WHILE i < n_rows DO
        SELECT str FROM tmp_splitted_str LIMIT i,1 INTO genre;

        INSERT INTO tmp_result
        SELECT * FROM
        (
            WITH movies_numbered AS (
                SELECT
                   m.movieId,
                   m.title,
                   m.genres,
                   m.year,
                   ROUND(AVG(r.rating), 1) AS 'rating',
                    ROW_NUMBER() over (ORDER BY r.rating) AS 'rn'
                FROM
                     movies AS m
                INNER JOIN ratings AS r
                    ON m.movieId = r.movieId
                WHERE
                    ((year_from IS NULL) OR (m.year >= year_from))
                AND ((year_to IS NULL) OR (m.year <= year_to))
                AND ((`regexp` IS NULL) OR (REGEXP_SUBSTR(m.title,`regexp`) != ''))
                AND REGEXP_SUBSTR(m.genres, genre) != ''
                GROUP BY
                         m.movieId,
                         m.title,
                         m.genres,
                         m.year
                ORDER BY
                         AVG(r.rating) DESC
            )
            SELECT movieId,
                    title,
                    mn.genres,
                    year,
                   rating
            FROM movies_numbered AS mn
            WHERE ((n IS NULL) OR (rn <= n))

        ) as insert_movies_genre;

      SET i = i + 1;
    END WHILE;

    SELECT * FROM tmp_result;

    DROP TABLE tmp_result;
    DROP TABLE tmp_splitted_str;
END;

CALL spr_find_top_rated_movies('5', 'the', 1995, 2005, 'Horror|Children');