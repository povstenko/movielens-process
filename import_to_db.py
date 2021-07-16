"""Import CSV to DB

This script allows user to import data to Database.

This file can also be imported as a module and contains the following
functions:
    * import_ratings_csv_to_db - Read data from CSV file and insert it to database table
    * import_movies_csv_to_db - Read data from CSV file and insert it to database table
    * main - the main function of the script
"""

# import the necessary packages
import re
import csv
import time
import logging as log
from config import *
from mysql.connector import (connection)


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
            log.debug(f"Reading file '{file_path}'")
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
        cnx.commit()
    except Exception as e:
        log.exception(e)
        cnx.rollback()
    
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
            log.debug(f"Reading file '{file_path}'")
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
                    log.warning(f'NULL genre: {row}')
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
        cnx.commit()
    except Exception as e:
        log.exception(e)
        log.debug(query_string)
        cnx.rollback()
    
    log.info(f'Rows affected: {rows_affected}')
    cursor.close()


def main():
    log.basicConfig(level=log.getLevelName(CONFIG['logging']['level']),
                    filename=CONFIG['logging']['filename'],
                    filemode=CONFIG['logging']['filemode'],
                    format=CONFIG['logging']['format'],
                    datefmt=CONFIG['logging']['datefmt'])
    log.info('Start')
    # save start time for calculating
    time_start = time.perf_counter()

    try:
        # DB connect
        log.info('Opening connection to DB')
        cnx = connection.MySQLConnection(**CONFIG['db_connect'])
        log.info('Done!')

        log.info('importing ratings to DB')
        import_ratings_csv_to_db(cnx, CONFIG['data_folder_path'] + 'ratings.csv')
        log.info('Done!')

        log.info('importing movies to DB')
        import_movies_csv_to_db(cnx, CONFIG['data_folder_path'] + 'movies.csv')
        log.info('Done!')

    except Exception as e:
        log.exception(e)

    cnx.close()
    log.info('Connection to DB closed')

    time_elapsed = time.perf_counter() - time_start
    log.info(f'Finish in {time_elapsed:.4f} secs')


if __name__ == "__main__":
    main()
