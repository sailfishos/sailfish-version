if [ -f /etc/os-release ]; then
    . /etc/os-release
    echo ",---"
    echo "| $PRETTY_NAME"
    echo "'---"
else
    echo "WARNING: No /etc/os-release found."
fi
