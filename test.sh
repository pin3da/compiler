#!/bin/sh
#
#   Manuel Pineda, test lexer
#

if [ $# -gt 0 ];then
    python mpaslex.py $1
else
    for i in test[0-9]*.in
    do
        python mpaslex.py $i > log 2> /dev/null
        if [ $? -gt 0 ]; then
            echo "\n*** ERROR DETECTED! look at" $i "***\n"
        fi
    done
fi 
