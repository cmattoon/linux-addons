#!/bin/bash
function _print() {
    local msg="$1"
    local c=${2-0}
    echo -e "\033[1m[\033[1;${c}m${msg}\033[0;1m]\033[0m"
}
ERROR=$(_print "  ERROR ! " "31")
INFO=$(_print "   INFO   " "36")
DEBUG=$(_print "  DEBUG   " "37")
ALERT=$(_print "  ALERT ! " "33")
OK=$(_print "   -OK-   " "32")
WARNING=$(_print " WARNING  " "33")
CRITICAL=$(_print " CRITICAL " "31")
FAILED=$(_print "  FAILED  " "31")
echo "$OK"
echo "$INFO"
echo "$DEBUG"
echo "$WARNING"
echo "$ALERT"
echo "$ERROR"
echo "$FAILED"
echo "$CRITICAL"

function fatal() {
    local message="$1"
    local code=${2-1}
    echo -e "${ERROR} ${message}\033[0m"
    exit $e;
}