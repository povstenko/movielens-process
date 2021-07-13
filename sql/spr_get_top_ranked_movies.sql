DROP PROCEDURE IF EXISTS spr_find_top_rated_movies;
CREATE PROCEDURE spr_find_top_rated_movies(
    IN n int,
    IN `regexp` varchar(200),
    IN year_from int,
    IN year_to int,
    IN genres varchar(200)
)
BEGIN
    SET SQL_SELECT_LIMIT = n;

    SELECT
           m.movieId,
           m.title,
           m.genres,
           m.year,
           ROUND(AVG(r.rating), 1) AS 'rating'
    FROM
         movies AS m
    INNER JOIN ratings AS r
        ON m.movieId = r.movieId
    WHERE
        ((year_from IS NULL) OR (m.year >= year_from))
    AND ((year_to IS NULL) OR (m.year <= year_to))
    AND ((`regexp` IS NULL) OR (REGEXP_SUBSTR(m.title,`regexp`) != ''))
    AND ((genres IS NULL) OR (REGEXP_SUBSTR(m.genres, genres) != ''))
    GROUP BY
             m.movieId,
             m.title,
             m.genres,
             m.year
    ORDER BY
             AVG(r.rating) DESC;

    SET SQL_SELECT_LIMIT = Default;
END;

CALL spr_find_top_rated_movies(5, 'Toy', 1995, 2005, 'Animation');