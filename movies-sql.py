"""Get top N rated movies from MovieLens

This script allows user to get information about films.

This file can also be imported as a module and contains the following
functions:

    * print_movies - Print data in csv format
    * get_arguments - Construct the argument parser and get the arguments
    * main - the main function of the script
"""

# import the necessary packages
import time
import argparse
import logging as log
from config import *
from mysql.connector import (connection)


def print_movies(cnx, n=None, regexp=None, year_from=None, year_to=None, genres=None, delimiter=','):
    """ Get and print movies from stored procedure

    Parameters
    ----------
    cnx :
        MySqlConnection to database
    n : int, optional
        The number of top rated movies for each genre, by default None
    regexp : str, optional
        Filter on name of the film, by default None
    year_from : int, optional
        The lower boundary of year filter, by default None
    year_to : int, optional
        The lower boundary of year filter, by default None
    genres : str, optional
        User-defined genre filter. can be multiple, by default None
    delimiter : str, optional
        Separator of csv format, by default ','
    """
    cursor = cnx.cursor()

    # NULL if None
    if not n:
        n = 'NULL'
    if not regexp:
        regexp = 'NULL'
    else:
        regexp = f"'{regexp}'"
    if not year_from:
        year_from = 'NULL'
    if not year_to:
        year_to = 'NULL'
    if not genres:
        genres = ['NULL']
    else:
        genres = genres.split('|')
        genres = [f"'{g}'" for g in genres]

    try:
        column_names = ['movieId', 'title', 'genres', 'year', 'rating']
        header = ', '.join(column_names)
        print(header)

        for genre in genres:
            query_string = f"CALL spr_find_top_rated_movies({n}, {regexp}, {year_from}, {year_to}, {genre});"
            for result in cursor.execute(query_string, multi=True):

                if result.with_rows:
                    log.debug(
                        f'Rows produced by statement "{result.statement}":')

                    for row in result.fetchall():
                        log.debug(row)

                        csv_row = ''
                        for attr in row:
                            if delimiter in str(attr):
                                attr = f'"{attr}"'
                            csv_row += delimiter + str(attr)
                        csv_row = csv_row[1:]
                        print(csv_row)
    except Exception as e:
        log.exception(e)

    cursor.close()


def get_arguments() -> dict:
    """Construct the argument parser and get the arguments

    Returns
    -------
    dict
        Dictionary of arguments and paramenters
    """
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("-n", "--topN", type=int,
                    help="the number of top rated movies for each genre. (example: 3)")
    ap.add_argument("-g", "--genres", type=str,
                    help="user-defined genre filter. can be multiple. (example: Comedy|Adventure)")
    ap.add_argument("-f", "--year_from", type=int,
                    help="the lower boundary of year filter (example: 1980)")
    ap.add_argument("-t", "--year_to", type=int,
                    help="the lower boundary of year filter (example: 2010)")
    ap.add_argument("-r", "--regexp", type=str,
                    help="filter on name of the film (example: love)")

    return vars(ap.parse_args())


def main():
    log.basicConfig(level=log.getLevelName(CONFIG['logging']['level']),
                    filename=CONFIG['logging']['filename'],
                    filemode=CONFIG['logging']['filemode'],
                    format=CONFIG['logging']['format'],
                    datefmt=CONFIG['logging']['datefmt'])
    log.info('Start')
    # save start time for calculating
    time_start = time.perf_counter()

    # construct args
    log.info('constructing argument parser')
    args = get_arguments()
    log.debug(f'arguments: {args}')
    log.info('Done!')

    try:
        # DB connect
        log.info('Opening connection to DB')
        cnx = connection.MySQLConnection(**CONFIG['db_connect'])
        log.info('Done!')

        log.info('fetching movies')
        print_movies(cnx, args['topN'], args['regexp'],
                     args['year_from'], args['year_to'], args['genres'])
        log.info('Done!')

    except Exception as e:
        log.error(e)

    cnx.close()
    log.info('Connection to DB closed')

    time_elapsed = time.perf_counter() - time_start
    log.info(f'Finish in {time_elapsed:.4f} secs')


if __name__ == "__main__":
    main()
