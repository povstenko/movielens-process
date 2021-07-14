CONFIG = {
    'data_folder_path': 'data/ml-latest-small/',
    'logging': {
        'level': 'DEBUG',
        'filename': 'log/import_to_db.log',
        'filemode': 'w',
        'format': '%(asctime)s - %(levelname)s - %(message)s',
        'datefmt': '%H:%M:%S'
    },
    'db_connect': {
        'user': 'root',
        'password': 'Nc38D8~!zu2P',
        'host': 'localhost',
        'database': 'movies_db',
        'raise_on_warnings': True
    }
}
