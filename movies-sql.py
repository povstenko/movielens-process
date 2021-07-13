import re
import csv
import time
import argparse
import logging as log
from mysql.connector import (connection)
from mysql.connector import Error
from mysql.connector.errorcode import ER_SLAVE_SILENT_RETRY_TRANSACTION


DATA_FOLDER_PATH = 'data/ml-latest-small/'
CONFIG = {
    'user': 'root',
    'password': 'Nc38D8~!zu2P',
    'host': 'localhost',
    'database': 'movies_db',
    'raise_on_warnings': True
}


def import_ratings_csv_to_db(cnx, file_path: str, delimiter=',', dest_table='ratings', skip_header=True) -> None:
    """Read data from CSV file and insert it to database table

    Parameters
    ----------
    cnx :
        MySqlConnection to database
    file_path : str
        File name of csv file
    delimiter : str, optional
        Delimiter of csv file, by default ','
    dest_table : str, optional
        Destination table name, by default 'ratings'
    skip_header : bool, optional
        Flag to determinate header row of file, by default True
    """
    cursor = cnx.cursor()

    try:
        with open(file_path, newline='') as csvfile:
            reader = csv.reader(csvfile, delimiter=delimiter)

            field_names = ''
            if skip_header:
                field_names = '(' + ', '.join(next(reader)) + ')'
            log.debug(field_names)

            rows_affected = 0
            for row in reader:
                values = ', '.join(row)
                query_string = f'INSERT INTO {dest_table} {field_names} VALUES ({values})'
                cursor.execute(
                    query_string,
                    values
                )
                rows_affected += cursor.rowcount
    except Exception as e:
        log.exception(e)

    cnx.commit()
    log.info(f'Rows affected: {rows_affected}')
    cursor.close()


def import_movies_csv_to_db(cnx, file_path: str, delimiter=',', dest_table='movies', skip_header=True, split_regex=r'\s\(\d{4}\)', year_regex=r'\d{4}', null_genre='(no genres listed)') -> None:
    """Read data from CSV file and insert it to database table

    Parameters
    ----------
    cnx :
        MySqlConnection to database
    file_path : str
        File name of csv file
    delimiter : str, optional
        Delimiter of csv file, by default ','
    dest_table : str, optional
        Destination table name, by default 'movies'
    skip_header : bool, optional
        Flag to determinate header row of file, by default True
    split_regex : str, optional
        Regular Expression used to remove substring from title column, by default r'\s\(\d{4}\)'
    year_regex : str, optional
        Regular Expression used to extract year from title column, by default r'\d{4}'
    null_genre : str, optional
        String that determinate NULL value of genres column, by default (no genres listed)'
    """
    cursor = cnx.cursor()

    try:
        with open(file_path, newline='') as csvfile:
            reader = csv.reader(csvfile, delimiter=delimiter)

            field_names = ''
            if skip_header:
                field_names = '(' + ', '.join(next(reader)+['year']) + ')'
            log.debug(field_names)

            rows_affected = 0
            for row in reader:

                # get year column from title
                year = re.search(split_regex, row[1])
                if year:
                    row[1] = re.sub(split_regex, '', row[1])
                    year = re.search(year_regex, year.group()).group()
                else:
                    year = 'NULL'
                    log.warning(f'Can`t split year column in row: {row}')
                row.append(year)

                row[1] = re.sub(r'\"', '\\"', row[1])
                row[1] = f'"{row[1]}"'

                # set NULL if no genres listed
                if row[2] == null_genre:
                    row[2] = 'NULL'
                else:
                    row[2] = f'"{row[2]}"'

                values = ', '.join(row)
                query_string = f'INSERT INTO {dest_table} {field_names} VALUES ({values})'
                # log.debug(query_string)
                cursor.execute(
                    query_string,
                    values
                )
                rows_affected += cursor.rowcount
    except Exception as e:
        log.exception(e)
        log.debug(query_string)

    cnx.commit()
    log.info(f'Rows affected: {rows_affected}')
    cursor.close()


def get_movies(cnx, n=None, regexp=None, year_from=None, year_to=None, genres=None, delimiter=','):
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
        for genre in genres:
            query_string = f"CALL spr_find_top_rated_movies({n}, {regexp}, {year_from}, {year_to}, {genre});"
            for result in cursor.execute(query_string, multi=True):
                if result.with_rows:
                    log.debug(f'Rows produced by statement "{result.statement}":')
                    
                    output = result.fetchall()
                    for row in output:
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
    log.basicConfig(level=log.DEBUG,
                    filename='log/sql.log',
                    filemode='w',
                    format='%(asctime)s - %(levelname)s - %(message)s',
                    datefmt='%H:%M:%S')
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
        cnx = connection.MySQLConnection(**CONFIG)
        log.info('Done!')

        # log.info('import ratings to DB')
        # import_ratings_csv_to_db(cnx, DATA_FOLDER_PATH + 'ratings.csv')
        # log.info('Done!')

        # log.info('import movies to DB')
        # import_movies_csv_to_db(cnx, DATA_FOLDER_PATH + 'movies.csv')
        # log.info('Done!')

        log.info('fetching movies')
        get_movies(cnx, args['topN'], args['regexp'],
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
