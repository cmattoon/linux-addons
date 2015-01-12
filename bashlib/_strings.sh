
##
# Converts a string to lowercase.
# username="$(lowercase $username)"
# Args:
#   - The string to convert
function lowercase() {
    local str="$@"
    local output
    output=$(tr '[A-Z]' '[a-z]'<<<"${str}")
    echo "$output"
}

