if shopt -q login_shell; then
    if [ -f /etc/os-release ]; then
        . /etc/os-release
        echo ",---"
        echo "| $PRETTY_NAME"
        echo "'---"
    else
        echo "Arrr, you're screwed, mate"
    fi
fi
