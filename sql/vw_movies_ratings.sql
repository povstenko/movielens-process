DROP VIEW IF EXISTS vw_movies_ratings;
CREATE VIEW vw_movies_ratings AS
    SELECT
        m.movieId,
        m.title,
        m.genres,
        m.year,
        AVG(r.rating)AS 'rating'
    FROM
        movies AS m
    INNER JOIN ratings AS r
        ON m.movieId = r.movieId
    GROUP BY
        m.movieId,
        m.title,
        m.genres,
        m.year;

-- SELECT * FROM vw_movies_ratings;