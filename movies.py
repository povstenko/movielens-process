

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
        Flag to determinate order of sorting, by default True

    Returns
    -------
    list
        Sorted data stored in list of dicts
    """
    return sorted(data, key=lambda k: k[sort_by], reverse=reverse)


def get_groupped_data(data: list,  group_by: str, agg_column: str, agg_function='mean') -> list:
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


def main():
    args = construct_argument_parser()

    # check if user don't pass any arguments
    if not any(args.values()):
        print('Pass arguments')
        exit()

    movies = read_csv('data/movies.csv')
    data_info(movies)
    # print(movies[:5])
    ratings = read_csv('data/ratings.csv')
    data_info(ratings)
    # print(ratings[:2])

    sorted_ratings = get_sorted_data(ratings, 'movieId')
    # print(sorted_ratings[:2])

    groupped_ratings = get_groupped_data(sorted_ratings, 'movieId', 'rating')
    
    
    groupped_ratings = get_sorted_data(groupped_ratings, 'movieId', reverse=False)
    print(groupped_ratings[:5])

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
