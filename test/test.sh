#!/bin/bash
#
#   Manuel Pineda, test lexer
#

if [ $# -gt 0 ];then
	if [ "$1" = "-all" ];then
	    check="true"
		for i in test[0-9]*.*
		do
		    python ../mpaslex.py $i > log
		    if [ $? -gt 0 ]; then
		        echo "*** ERROR DETECTED! look at" $i "***"
		        check="false"
		    fi
		done
		if [ "$check" = "true" ];then
			echo "*** All tests checked ***"
		fi
	else
		python ../mpaslex.py $1 > log
	fi
else
	check="true"
    for i in test[0-9]*.correct
    do
        python ../mpaslex.py $i > log 
        if [ $? -gt 0 ]; then
            echo "*** ERROR DETECTED! look at" $i "***"
            check="false"
        fi
    done
    if [ "$check" = "true" ];then
    	echo "*** All tests checked ***"
    fi
fi 
