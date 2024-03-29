#!/bin/bash

# Check if directory argument is provided
if [ $# -ne 1 ]; then
    echo "Usage: $0 <directory>"
    exit 1
fi

# Check if the provided directory exists
if [ ! -d "$1" ]; then
    echo "Error: Directory '$1' not found."
    exit 1
fi

# Iterate through all .py files in the directory and run python3 <FILE> -h
for file in "$1"/*.py; do
    if [ -f "$file" ]; then
        echo "#### \`$(basename "$file")\`"
        echo '```'
        python3 "$file" -h
        echo '```'
        echo ""
    fi
done
