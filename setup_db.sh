#!/bin/bash
#purpose: creating database for application
#author:  Vitaliy Povstenko
#date:    17/07/2021

function parse_arguments() {
    while getopts h:P:u:p:d: flag
    do
        case "${flag}" in
            h) host_arg=${OPTARG};;
            P) port=${OPTARG};;
            u) user=${OPTARG};;
            p) pass=${OPTARG};;
            d) db=${OPTARG};;
        esac
    done
}

function execute_sql_files() {
    export MYSQL_PWD=$pass;
    
    mysql -h $host_arg --port=$port $db -u$user < sql/movies_table.sql
    echo "sql/movies_table.sql Executed"
    
    mysql -h $host_arg --port=$port $db -u$user < sql/ratings_table.sql
    echo "sql/ratings_table.sql Executed"
    
    mysql -h $host_arg --port=$port $db -u$user < sql/spr_split_str.sql
    echo "sql/spr_split_str.sql Executed"
    
    mysql -h $host_arg --port=$port $db -u$user < sql/spr_get_top_ranked_movies.sql
    echo "sql/spr_get_top_ranked_movies.sql Executed"
}

###################
##    MAIN      ###
###################
parse_arguments "$@";
execute_sql_files;

#END