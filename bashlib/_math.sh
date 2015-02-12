#!/bin/bash

##
# Compares two strings as float values
# Suitable for use in conditionals.
#
# $1: Float #1
# $2: Float #2
# Returns: True (0) if $1 < $2, else False (1)
function floatcompare() {
    awk -v n1=$1 -v n2=$2 'BEGIN { if (n1 < n2) exit 0; exit 1; }'
}


