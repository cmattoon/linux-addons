#!/bin/bash
##
# Echos a line with a given color code.
# $1: The string to print
# $2: The color code (e.g., 91=Red)
exitscript() {
#    exit ${1-0} && exit ${1-0}
    exit ${1-0}
}
_color() {
    local msg="$1"
    local c=${2-0}
    echo -e "\033[0m\033[${c}m[${msg}]\033[0m"
}
ERROR=$(_color "  ERROR ! " "31")
INFO=$(_color "   INFO   " "36")
DEBUG=$(_color "  DEBUG   " "37")
ALERT=$(_color "  ALERT ! " "33")
OK=$(_color "   -OK-   " "32")
WARNING=$(_color " WARNING  " "33")
CRITICAL=$(_color " CRITICAL " "31")
FAILED=$(_color "  FAILED  " "31")

# echo "$ERROR"
# echo "$INFO"
# echo "$DEBUG"
# echo "$ALERT"
# echo "$OK"
# echo "$WARNING"
# echo "$CRITICAL"
# echo "$FAILED"

##
# Prints an error message and exits.
# $1: The string to print
# $2: The exit code (default 1)
#


printok() {
    echo -e "${OK} ${1:-\"\"}\033[0m"
}

printfailed() {
    echo -e "${FAILED} ${1:-\"\"}\033[0m"
}

printdebug() {
    echo -e "${DEBUG} ${1:-\"\"}\033[0m"
}

printinfo() {
    echo -e "${INFO} ${1:-\"\"}\033[0m"
}

printwarning() {
    echo -e "${WARNING} ${1:-\"\"}\033[0m"
}

printcritical() {
    echo -e "${CRITICAL} ${1:-\"\"}\033[0m"
}

printfatal() {
    echo -e "${ERROR} ${1:-\"\"}\033[0m"
    exitscript ${2:-1}
}