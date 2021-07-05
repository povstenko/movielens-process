

# import the necessary packages
import csv
import argparse
from itertools import groupby
from statistics import mean


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
    return sorted(data, key=lambda k: k[sort_by], reverse=reverse)


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


def construct_argument_parser() -> dict:
    """Construct the argument parser and get the arguments

    Returns
    -------
    dict
        Dictionary of arguments and paramenters
    """
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("-n", "--topN", type=str,
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
    merged_data = []
    for row_left in data_left:
        for row_right in data_right:
            if row_left[join_on] == row_right[join_on]:
                merged_data.append({**row_left, **row_right})
                break
    
    return merged_data


def main():
    args = construct_argument_parser()

    # check if user don't pass any arguments
    if not any(args.values()):
        print('Pass arguments')
        exit()

    movies = read_csv('data/movies.csv')
    # data_info(movies)
    # print(movies[:5])
    ratings = read_csv('data/ratings.csv')
    # data_info(ratings)
    # print(ratings[:2])

    sorted_ratings = get_sorted_data(ratings, 'movieId')
    # print(sorted_ratings[:2])

    groupped_ratings = get_groupped_data(sorted_ratings, 'movieId', 'rating')
    
    
    # sort datasets before merge
    sorted_movies = get_sorted_data(movies, 'movieId', reverse=False)
    print(sorted_movies[:3])
    data_info(sorted_movies)
    sorted_ratings = get_sorted_data(groupped_ratings, 'movieId', reverse=False)
    print(sorted_ratings[:3])
    data_info(sorted_ratings)

    
    merged_data = merge_two_datasets(sorted_movies, sorted_ratings, 'movieId')
    print(merged_data[:3])
    data_info(merged_data)
    
    # if args['topN']:
    #     print('topN')

    # if args['genres']:
    #     print('genres')

    # if args['year_from']:
    #     print('year_from')

    # if args['year_to']:
    #     print('year_to')

    # if args['regexp']:
    #     print('regexp')


if __name__ == "__main__":
    main()
