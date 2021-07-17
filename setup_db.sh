#!/bin/bash
#purpose: creating database for application
#author:  Vitaliy Povstenko
#date:    17/07/2021

host="127.0.0.1"
port="3307"
user="client"
pass="DCCcuons"
db="movies_db"

mysql -h $host --port=$port -u$user -p$pass < sql/movies_db.sql
mysql -h $host --port=$port $db -u$user -p$pass < sql/movies_table.sql
mysql -h $host --port=$port $db -u$user -p$pass < sql/ratings_table.sql
mysql -h $host --port=$port $db -u$user -p$pass < sql/spr_split_str.sql
mysql -h $host --port=$port $db -u$user -p$pass < sql/spr_get_top_ranked_movies.sql
