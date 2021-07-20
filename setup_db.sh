#!/bin/bash
#purpose: creating database for application
#author:  Vitaliy Povstenko
#date:    17/07/2021

function parse_arguments() {
    if [ $# -eq 0 ]
    then
        echo "No arguments supplied"
        exit 1
    fi

    while getopts "h:P:u:p:d:" flag
    do
        case "${flag}" in
            h) checkargs
                host_arg=${OPTARG};;
            P) checkargs
                port=${OPTARG};;
            u) checkargs
                user=${OPTARG};;
            p) checkargs
                pass=${OPTARG};;
            d) checkargs
                db=${OPTARG};;
            *) echo "No reasonable options found!" 
                exit 1;;
        esac
    done
}

checkargs () {
    if echo "$OPTARG" | grep -q '^-';
    then
        echo "Unknown argument $OPTARG for option $opt!"
        exit 1
    fi
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