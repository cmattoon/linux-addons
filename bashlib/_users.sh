#!/bin/bash

##
# Checks if the script is being run as root.
# @return bool
#
function is_root() {
    [ $(id -u) -eq 0 ] && return $TRUE || return $FALSE
}

##
# Checks if user exists
# @$1 username The username to check in /etc/passwd
# @return bool
#
function user_exists() {
    local user="$1"
    grep -q "^${user}" /etc/passwd && return $TRUE || return $FALSE
}