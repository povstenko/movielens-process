

# import the necessary packages
import csv
import argparse


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
    print(movies[:5])
    ratings = read_csv('data/ratings.csv')
    print(ratings[:5])

    if args['topN']:
        print('topN')

    if args['genres']:
        print('genres')

    if args['year_from']:
        print('year_from')

    if args['year_to']:
        print('year_to')

    if args['regexp']:
        print('regexp')


if __name__ == "__main__":
    main()
