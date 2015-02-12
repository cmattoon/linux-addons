#!/bin/bash


# Abspath
# Returns absolute path of given path. 
# Usage: path=$(abspath foo)
#
abspath() {
    local relpath=${1:-$(pwd)}
    local abspath=$(cd $relpath && pwd)
    echo "${abspath}"
}

