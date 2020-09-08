is_login_shell() [ "$0" != "${0#-}" ]
if is_login_shell; then
    if [ -f /etc/os-release ]; then
        . /etc/os-release
        echo ",---"
        echo "| $PRETTY_NAME"
        echo "'---"
    else
        echo "WARNING: No /etc/os-release found."
    fi
fi
unset -f is_login_shell
