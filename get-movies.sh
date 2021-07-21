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

    while getopts "h:n:g:f:t:r:" flag
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
    echo "  -h (help) show this message and exit"
    echo "  -n (topN) the number of top rated movies for each genre (example: 3)"
    echo "  -g (genres) user-defined genre filter. can be multiple. (example: \"Comedy|Adventure\")"
    echo "  -f (year_from) the lower boundary of year filter (example: 1980)"
    echo "  -t (year_to) the lower boundary of year filter (example: 2010)"
    echo "  -r (regexp) filter on name of the film (example: love)"
}

function get_movies() {
    python3 movies-client.py -n $topN -g $genres -f $year_from -t $year_to -r $regexp
    # python3 movies-client.py -n 5 -g "Comedy|Animation" -f 1990 -t 2010 -r the
}



###################
##    MAIN      ###
###################
parse_arguments "$@";
get_movies;

#END