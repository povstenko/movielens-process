-- --------------------------------------------------------

--
-- Структура таблицы `ratings`
--
DROP TABLE IF EXISTS `ratings`;
CREATE TABLE `ratings` (
  `userId` int(11) NOT NULL,
  `movieId` int(11) NOT NULL,
  `rating` float NOT NULL,
  `timestamp` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;