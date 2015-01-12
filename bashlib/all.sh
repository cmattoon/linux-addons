#!/bin/bash
#################################################################################################
## Include this file, which will include the rest.
## Keep them all in the same directory.
##
cwd=$(cd $(dirname "${BASH_SOURCE[0]}") && pwd)
script="$cwd/$(basename ${BASH_SOURCE[0]})"

source "${cwd}/_definitions.sh"
source "${cwd}/_strings.sh"
source "${cwd}/_params.sh"
source "${cwd}/_messages.sh"
source "${cwd}/_users.sh"

