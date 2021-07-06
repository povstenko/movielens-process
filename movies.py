

# import the necessary packages
import csv
import argparse
from itertools import groupby
from statistics import mean
import re


def read_csv(file_path: str, delimiter: str = ',') -> list:
    """Read data from CSV file and return it as a list

    Parameters
    ----------
    file_path : str
        File name of csv file
    delimiter : str, optional
        Delimiter of csv file, by default ','

    Returns
    -------
    list
        Data from file stored in list of dicts with column names as a keys
    """
    data = []
    with open(file_path, newline='') as csvfile:
        reader = csv.DictReader(csvfile, delimiter=delimiter)
        for row in reader:
            data.append(row)

    return data


def print_data_csv(data: list, delimiter=',', n_rows=None) -> None:
    """Print data in csv format

    Parameters
    ----------
    data : list
        Data stored in list of dict
    delimiter : str, optional
        Separator of csv format, by default ','
    n_rows : [type], optional
        Number of rows to display, by default None
    """
    if n_rows:
        data = data[:n_rows]

    header = ''
    for k, v in data[0].items():
        header += delimiter + k
    header = header[1:]
    print(header)

    for row in data:
        csv_row = ''
        for k, v in row.items():
            csv_row += delimiter + str(v)
        csv_row = csv_row[1:]
        print(csv_row)


def data_info(data: list) -> None:
    """Print data summary info

    Parameters
    ----------
    data : list
        Data stored in list of dicts
    """
    cols = list(data[0].keys())
    print(f'Columns: {cols} \
        \nNumber of columns: {len(cols)} \
        \nNumber of rows: {len(data)}\n')


def get_sorted_data(data: list, sort_by: str, reverse=True) -> list:
    """Get sorted data by column and order

    Parameters
    ----------
    data : list
        Data stored in list of dicts
    sort_by : str
        Sort data by specific column
    reverse : bool, optional
        Flag to determinate order of sorting (False - asc, True - desc), by default True

    Returns
    -------
    list
        Sorted data stored in list of dicts
    """
    return sorted(data, key=lambda k: (k[sort_by] is not None, k[sort_by]), reverse=reverse)


def get_groupped_data(data: list,  group_by: str, agg_column: str, agg_function='mean') -> list:
    """Group data by column and apply aggregation function

    Parameters
    ----------
    data : list
        Data stored in list of dicts
    group_by : str
        Column of groupping operation
    agg_column : str
        Column of aggregation
    agg_function : str, optional
        Aggregation function, by default 'mean'

    Returns
    -------
    list
        Groupped data stored in list of dicts
    """
    groupped_data = []

    for k, v in groupby(data, key=lambda x: x[group_by]):
        group_row = {group_by: k}
        agg_vals = [float(i[agg_column]) for i in v]
        group_row[agg_column] = round(mean(agg_vals), 1)
        groupped_data.append(group_row)

    return groupped_data


def merge_two_datasets(data_left: list, data_right: list, join_on: str) -> list:
    """Merge Join two sorted datasets (tables) into one on unique key

    Parameters
    ----------
    data_left : list
        Left data stored in list of dicts 
    data_right : list
        Right data stored in list of dicts
    join_on : str
        Common unique column key of two datasets

    Returns
    -------
    list
        Merged data stored in list of dicts
    """
    # data right columns with None values in case when right table don`t match left
    columns_right = list(data_right[0])
    columns_right.remove(join_on)
    right_none = dict.fromkeys(columns_right, None)

    merged_data = []
    for row_left in data_left:
        merged_row = {**row_left, **right_none}
        for row_right in data_right:
            if row_left[join_on] == row_right[join_on]:
                merged_row = {**row_left, **row_right}
                break
        merged_data.append(merged_row)

    return merged_data


def get_factorized_data(data: list, column: str, delimiter=',') -> list:
    """Factorize column of data which contains multiple 
    categorical data by splitting it on list of categories

    Parameters
    ----------
    data : list
        Data stored in list of dicts
    column : str
        Column name to factorize
    delimiter : str, optional
        Delimiter of values in column, by default ','

    Returns
    -------
    list
        Factorized data stored in list of dicts
    """
    # factorized_data = []

    for row in data:
        row[column] = row[column].split(delimiter)

    return data


def get_categories_of_column(data: list, column: str, delimiter=',') -> list:
    """Get list of unique categories of non-atomic column which contains
    multiple categorical values splitted by delimiter

    Parameters
    ----------
    data : list
        Data stored in list of dicts
    column : str
        Column name which contains multiple values
    delimiter : str, optional
        Delimiter of values in column, by default ','

    Returns
    -------
    list
        Unique list of categories in variable
    """
    column_values = ''
    for row in data:
        column_values += delimiter + str(row[column])

    splitted = column_values.split(delimiter)[1:]
    categories = list(set(splitted))

    return categories


def split_data_column(data: list, column: str, new_column: str, old_col_regex: str, new_col_regex: str) -> list:
    """Split column of data and create new column by regular expression

    Parameters
    ----------
    data : list
        Data stored in list of dicts
    column : str
        Column name you need to split
    new_column : str
        New column name 
    old_col_regex : str
        RegEx used to remove data from first column
    new_col_regex : str
        RegEx used to create new column

    Returns
    -------
    list
        Data stored in list of dicts
    """
    for row in data:
        if re.search(new_col_regex, row[column]):
            new_col_val = re.search(new_col_regex, row[column]).group()
        else:
            new_col_val = None
        row[new_column] = new_col_val
        row[column] = re.sub(old_col_regex, '', row[column])

    return data


def filter_data_column_contains(data: list, column: str, substring: str) -> list:
    """Filter data in condition if column contains substring

    Parameters
    ----------
    data : list
        Data stored in list of dicts
    column : str
        Filtering column
    substring : str
        Substring of column value

    Returns
    -------
    list
        Filtered data stored in list of dicts
    """
    filtered_data = []

    for row in data:
        if re.search(substring, row[column]):
            filtered_data.append(row)

    return filtered_data


def vertical_stack_data(data_top: list, data_bottom: list) -> list:
    """Return vertically stacked data

    Parameters
    ----------
    data_top : list
        First data stored in list of dicts
    data_bottom : list
        Second data stored in list of dicts

    Returns
    -------
    list
        Stacked data
    """
    data_top.extend(data_bottom)
    return data_top


def data_sliced(data: list, start=None, end=None) -> list:
    """Dataset safe slicing method

    Parameters
    ----------
    data : list
        Data stored in list of dicts
    start : [type], optional
        Start index, by default None
    end : [type], optional
        End index, by default None

    Returns
    -------
    list
        Sliced data stored in list of dicts
    """
    if start:
        data = data[start:]
    if end:
        data = data[:end]
    return data


def construct_argument_parser() -> dict:
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
    args = construct_argument_parser()

    # check if user don't pass any arguments
    if not any(args.values()):
        print('Pass arguments')
        exit()

    movies = read_csv('data/movies.csv')
    # data_info(movies)
    # movies = get_categories_of_column(movies, 'genres', delimiter='|')
    # movies = get_factorized_data(movies, 'genres', delimiter='|')

    # get year column from title
    movies = split_data_column(movies, 'title', 'year',
                               r'\s\(\d\d\d\d\)', r'\d\d\d\d')

    movies = get_sorted_data(movies, 'movieId', reverse=False)
    # print_data_csv(movies, n_rows=5)

    ratings = read_csv('data/ratings.csv')
    # data_info(ratings)

    ratings = get_sorted_data(ratings, 'movieId', reverse=False)
    ratings = get_groupped_data(ratings, 'movieId', 'rating')

    # merge datasets
    data = merge_two_datasets(movies, ratings, 'movieId')
    data = get_sorted_data(data, 'rating', reverse=True)
    # data_info(data)

    # print_data_csv(data, n_rows=args['topN'])

    if args['year_from']:
        print(args['year_from'])

    if args['year_to']:
        print(args['year_to'])

    if args['regexp']:
        print(args['regexp'])

    if args['genres']:
        genres = args['genres'].split('|')
        stacked_data = []
        for genre in genres:
            stacked_data.extend(
                data_sliced(
                    filter_data_column_contains(data, 'genres', genre),
                    end=args['topN'])
                )
        print_data_csv(stacked_data)
    else:
        print_data_csv(data, n_rows=args['topN'])


if __name__ == "__main__":
    main()
