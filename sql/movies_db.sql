-- phpMyAdmin SQL Dump
-- version 5.0.2
-- https://www.phpmyadmin.net/
--
-- Хост: 127.0.0.1
-- Время создания: Июл 14 2021 г., 11:01
-- Версия сервера: 10.4.14-MariaDB
-- Версия PHP: 7.4.10

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- База данных: `movies_db`
--
CREATE DATABASE IF NOT EXISTS `movies_db` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;
USE `movies_db`;


-- --------------------------------------------------------

--
-- Структура таблицы `movies`
--

CREATE TABLE `movies` (
  `movieId` int(11) NOT NULL,
  `title` varchar(255) NOT NULL,
  `genres` varchar(255) DEFAULT NULL,
  `year` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;


-- --------------------------------------------------------

--
-- Структура таблицы `ratings`
--

CREATE TABLE `ratings` (
  `userId` int(11) NOT NULL,
  `movieId` int(11) NOT NULL,
  `rating` float NOT NULL,
  `timestamp` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;


DELIMITER $$
--
-- Процедуры
--
CREATE DEFINER=`root`@`localhost` PROCEDURE `spr_find_top_rated_movies` (IN `n` INT, IN `regexp` VARCHAR(200), IN `year_from` INT, IN `year_to` INT, IN `genre` VARCHAR(200))  BEGIN
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
    AND ((genres IS NULL) OR (REGEXP_SUBSTR(m.genres, genre) != ''))
    GROUP BY
             m.movieId,
             m.title,
             m.genres,
             m.year
    ORDER BY
             AVG(r.rating) DESC;

    SET SQL_SELECT_LIMIT = Default;
END$$

DELIMITER ;
