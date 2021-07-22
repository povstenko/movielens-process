#!/bin/bash
#purpose: wrapper for get-movies application
#author:  Vitaliy Povstenko
#date:    17/07/2021


function parse_arguments() {
    if [ $# -eq 0 ]
    then
        print_help;
        exit 0
    fi

    # default parameters
    hostname="localhost"
    port="3306"
    user="root"
    pass="root"
    db="master"

    while getopts "hn:g:f:t:r:sH:P:u:p:d:" flag
    do
        case "${flag}" in
            h)  
                checkargs
                print_help;
                exit 0;;
            n)  
                checkargs
                topN=${OPTARG};;
            g)  
                checkargs
                genres=${OPTARG};;
            f)  
                checkargs
                year_from=${OPTARG};;
            t)  
                checkargs
                year_to=${OPTARG};;
            r)
                checkargs
                regexp=${OPTARG};;
            s)
                checkargs
                setupdb=1;;
            H)  
                checkargs
                hostname=${OPTARG};;
            P)  
                checkargs
                port=${OPTARG};;
            u)
                checkargs
                user=${OPTARG};;
            p)  
                checkargs
                pass=${OPTARG};;
            d)
                checkargs
                db=${OPTARG};;
            \? )
                echo "Invalid Option"
                exit 1;;
            *) echo "No reasonable options found!" 
                exit 1;;
        esac
    done
}

function checkargs() {
    if echo "$OPTARG" | grep -q '^-';
    then
        echo "Unknown argument $OPTARG for option $opt"
        exit 1
    fi
}

function print_help() {
    echo "Get top N rated movies from MovieLens"
    echo ""
    echo "Usage:"
    echo "  ./get-movies.sh [-h] [-n TOPN] [-g GENRES] [-f YEAR_FROM] [-t YEAR_TO] [-r REGEXP]"
    echo "Optional arguments:"
    echo "  -help (help) show this message and exit"
    echo "  -n (topN) the number of top rated movies for each genre (example: 3)"
    echo "  -g (genres) user-defined genre filter. can be multiple. (example: \"Comedy|Adventure\")"
    echo "  -f (year_from) the lower boundary of year filter (example: 1980)"
    echo "  -t (year_to) the lower boundary of year filter (example: 2010)"
    echo "  -r (regexp) filter on name of the film (example: love)"
}

function exec_sql_files() {
    echo "Executing SQL files"
    export MYSQL_PWD=$pass;
    echo -ne '                          (0%)\r'

    mysql -h $hostname --port=$port $db -u$user < sql/movies_table.sql
    echo -ne '#######                   (25%)\r'

    mysql -h $hostname --port=$port $db -u$user < sql/ratings_table.sql
    echo -ne '#############             (50%)\r'

    mysql -h $hostname --port=$port $db -u$user < sql/vw_movies_ratings.sql
    echo -ne '#################         (75%)\r'

    mysql -h $hostname --port=$port $db -u$user < sql/spr_get_top_ranked_movies.sql
    echo -ne '#######################   (100%) Done!\r'
    echo -ne '\n'
}

function exec_import_to_db() {
    echo "Importing data to db"
    python3 import_to_db.py &
    PID=$!
    i=1
    sp="/-\|"
    echo -n ' '
    while [ -d /proc/$PID ]
    do
        printf "\b${sp:i++%${#sp}:1}"
    done
    echo ""
    echo "Done!"
}

function construct_command () {
    cmd="python3 movies-client.py"

    if [[ -v topN ]]
    then
        cmd="${cmd} -n ${topN}"
    fi

    if [[ -v genres ]]
    then
        cmd="${cmd} -g \"${genres}\""
    fi

    if [[ -v year_from ]]
    then
        cmd="${cmd} -f \"${year_from}\""
    fi

    if [[ -v year_to ]]
    then
        cmd="${cmd} -t \"${year_to}\""
    fi

    if [[ -v regexp ]]
    then
        cmd="${cmd} -r \"${regexp}\""
    fi
}


###################
##    MAIN      ###
###################
parse_arguments "$@";

if [[ -v setupdb ]];
then
    
    exec_sql_files;
    exec_import_to_db;
else
    construct_command;
    eval $cmd;
fi
#END