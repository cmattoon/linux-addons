#!/bin/bash


function floatcompare() {
    awk -v n1=$1 -v n2=$2 'BEGIN { if (n1 < n2) exit 0; exit 1; }'
}