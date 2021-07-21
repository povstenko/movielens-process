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
    WITH row_numbered AS
    (
        WITH RECURSIVE selected_genres(i, genre) AS
        (
            SELECT 1, SUBSTRING_INDEX(SUBSTRING_INDEX(genres, '|', 1), '|', -1) as genre
            UNION ALL
            SELECT i+1, SUBSTRING_INDEX(SUBSTRING_INDEX(genres, '|', i+1), '|', -1)
            FROM selected_genres
            WHERE i-1 < (CHAR_LENGTH(genres) - CHAR_LENGTH(REPLACE(genres, '|', '')))
        )
        SELECT
               *,
               ROW_NUMBER() OVER (
                   PARTITION BY
                       selected_genres.genre
                   ORDER BY
                       mr.rating DESC,
                       mr.year DESC,
                       mr.title
                   ) AS rn
        FROM selected_genres
        JOIN vw_movies_ratings mr
        ON REGEXP_SUBSTR(mr.genres, selected_genres.genre) != ''
    )
    SELECT
           *
    FROM row_numbered num
    WHERE
          ((year_from IS NULL) OR (num.year >= year_from))
      AND ((year_to IS NULL) OR (num.year <= year_to))
      AND ((`regexp` IS NULL) OR (REGEXP_SUBSTR(num.title, `regexp`) != ''))
      AND ((n IS NULL) OR (num.rn <= n))
    ORDER BY
             num.i,
             num.rating DESC,
             num.year DESC,
             num.title;
END;

-- CALL spr_find_top_rated_movies('5', NULL, 1995, 2015, 'Horror|Children');