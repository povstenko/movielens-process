DROP PROCEDURE IF EXISTS spr_find_top_rated_movies;
DELIMITER $$
CREATE PROCEDURE spr_find_top_rated_movies(
    IN n INT,
    IN `regexp` VARCHAR(200),
    IN year_from INT,
    IN year_to INT,
    IN genres VARCHAR(255)
)
BEGIN
    DECLARE n_rows INT DEFAULT 0;
    DECLARE i INT DEFAULT 0;
    DECLARE genre VARCHAR(100) DEFAULT 0;

    DROP TEMPORARY TABLE IF EXISTS tmp_result;
    CREATE TEMPORARY TABLE tmp_result(
        movieId INT,
        title VARCHAR(255),
        genres VARCHAR(255),
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
                    ROW_NUMBER() OVER (ORDER BY r.rating) AS 'rn'
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

-- CALL spr_find_top_rated_movies('5', 'the', 1995, 2005, 'Horror|Children');