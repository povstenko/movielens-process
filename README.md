
# Top MovieLens

[![GitHub](https://img.shields.io/badge/GitHub-100000)](https://github.com/povstenko/movielens-process)
[![Apache 2.0](https://img.shields.io/aur/license/android-studio.svg?)](https://www.apache.org/licenses/LICENSE-2.0/)

This script allows user to get information about top rated films.

## Table of Contents

- [Parameters](#parameters)
- [Usage](#usage)
  * [Get top N ranked movies](#get-top-n-ranked-movies)
  * [Search by title](#search-by-title)
  * [Filter by year](#filter-by-year)
  * [Top films for each genre](#top-films-for-each-genre)
  * [Saving output to file](#saving-output-to-file)
- [License](#license)

  

## Parameters

*  `-h`, `--help` show help message and exit
*  `-n`, `--topN` the number of top rated movies for each genre. *(example: 3)*
*  `-g`, `--genres` user-defined genre filter. can be multiple. *(example: "Comedy|Adventure")
*  `-f`, `--year_from` the lower boundary of year filter *(example: 1980)*
*  `-t`, `--year_to` the lower boundary of year filter *(example: 2010)*
*  `-r`, `--regexp` filter on name of the film *(example: love)*
 
## Usage

### Get top N ranked movies

Use `--topN` parameter to get top N ranked movies, for example, following command returns top 3 films:
```
$python movies.py -n 3
```
Output:
```
movieId,title,genres,year,rating
100556,Act of Killing, The,Documentary,2012,5.0
100906,Maniac Cop 2,Action|Horror|Thriller,1990,5.0
102084,Justice League: Doom ,Action|Animation|Fantasy,2012,5.0
```

###  Search by title
Pass [RegEx](https://en.wikipedia.org/wiki/Regular_expression) as a argument of `--regexp` to search by movie title.

For example, to get  top 2 films about "love" use command:
```
$python movies.py -n 2 -r love
```
Output:
```
movieId,title,genres,year,rating
2314,Beloved,Drama,1998,4.5
750,Dr. Strangelove or: How I Learned to Stop Worrying and Love the Bomb,Comedy|War,1964,4.3  
```

### Filter by year
Use `--year_from` and `year_from` to determinate movie\`s year range.

This command returns movies with "love" in title and the year is more or equal than 1995:
```
$python movies.py -r love -f 1995
```
Output:
```
movieId,title,genres,year,rating
2314,Beloved,Drama,1998,4.5
40,Cry, the Beloved Country,Drama,1995,4.2
152077,10 Cloverfield Lane,Thriller,2016,3.7
57368,Cloverfield,Action|Mystery|Sci-Fi|Thriller,2008,3.4
184253,The Cloverfield Paradox,Horror|Mystery|Sci-Fi|Thriller,2018,2.2
```

And following command returns movies with year between 1995 and 2008:
```
$python movies.py -r love -f 1995 -t 2008
```
Output:
```
movieId,title,genres,year,rating
2314,Beloved,Drama,1998,4.5
40,Cry, the Beloved Country,Drama,1995,4.2
57368,Cloverfield,Action|Mystery|Sci-Fi|Thriller,2008,3.4
```

###  Top films for each genre
Specify `--genres` argument in order to get top ranked films for each genre category.

For example, this command returns top 5 movies  from 2000 year for Comedy and Adventure genres:
```
$python movies.py -n 5 -f 2000 -g "Comedy|Adventure"
```
Output:
```
movieId,title,genres,year,rating
103602,Craig Ferguson: I'm Here To Help,Comedy|Documentary,2013,5.0
107951,Hunting Elephants,Comedy|Crime,2013,5.0
108078,Chinese Puzzle (Casse-tГЄte chinois),Comedy|Romance,2013,5.0
109241,On the Other Side of the Tracks (De l'autre cГґtГ© du pГ©riph),Action|Comedy|Crime,2012,5.0
113829,One I Love, The,Comedy|Drama|Romance,2014,5.0
108795,Wonder Woman,Action|Adventure|Animation|Fantasy,2009,5.0
124404,Snowflake, the White Gorilla,Adventure|Animation|Children|Comedy,2011,5.0
124851,Delirium,Adventure|Romance|Sci-Fi,2014,5.0
126921,The Fox and the Hound 2,Adventure|Animation|Children|Comedy,2006,5.0
146662,Dragons: Gift of the Night Fury,Adventure|Animation|Comedy,2011,5.0
```

### Saving output to file
Use `>` to specify filename and redirect output of script to the file.

For example:
```
$python movies.py -n 100 -f 1980 -t 2010 -g "Animation" > output.csv
```
Output:
```

```
output.csv:
```
movieId,title,genres,year,rating
104780,Mystery of the Third Planet, The (Tayna tretey planety),Adventure|Animation|Sci-Fi,1981,5.0
108795,Wonder Woman,Action|Adventure|Animation|Fantasy,2009,5.0
112512,Colourful (Karafuru),Animation|Drama|Fantasy|Mystery,2010,5.0
1151,Lesson Faust,Animation|Comedy|Drama|Fantasy,1994,5.0
...
```

## License

Apache 2.0 License: [www.apache.org/licenses/LICENSE-2.0](https://www.apache.org/licenses/LICENSE-2.0/) or see [the `LICENSE` file](https://github.com/povstenko/movielens-process/blob/main/LICENSE).
