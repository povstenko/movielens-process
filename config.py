CONFIG = {
    'data_folder_path': 'data/ml-latest-small/',
    'logging': {
        'level': 'DEBUG',
        'filename': 'log/client.log',
        'filemode': 'w',
        'format': '%(asctime)s - %(levelname)s - %(message)s',
        'datefmt': '%H:%M:%S'
    },
    'db_connect': {
        'user': 'client',
        'password': 'DCCcuons',
        'host': '127.0.0.1',
        'port': '3307',
        'database': 'movies_db',
        'raise_on_warnings': True
    }
}
