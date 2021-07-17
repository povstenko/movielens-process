#!/bin/bash
#purpose: creating database for application
#author:  Vitaliy Povstenko
#date:    17/07/2021

while getopts h:P:u:p:d: flag
do
    case "${flag}" in
        h) host=${OPTARG};;
        P) port=${OPTARG};;
        u) user=${OPTARG};;
        p) pass=${OPTARG};;
        d) db=${OPTARG};;
    esac
done

mysql -h $host --port=$port -u$user -p$pass < sql/movies_db.sql
mysql -h $host --port=$port $db -u$user -p$pass < sql/movies_table.sql
mysql -h $host --port=$port $db -u$user -p$pass < sql/ratings_table.sql
mysql -h $host --port=$port $db -u$user -p$pass < sql/spr_split_str.sql
mysql -h $host --port=$port $db -u$user -p$pass < sql/spr_get_top_ranked_movies.sql

#END