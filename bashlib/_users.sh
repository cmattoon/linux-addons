#!/bin/bash

##
# Checks if the script is being run as root.
# @return bool
#
is_root() {
    [ $(id -u) -eq 0 ] && return $(True) || return $(False)
}

##
# Checks if user exists
# @$1 username The username to check in /etc/passwd
# @return bool
#
user_exists() {
    local user="$1"
    grep -q "^${user}" /etc/passwd && return $(True) || return $(False)
}

