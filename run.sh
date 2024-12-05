#!/bin/bash
# This script runs the disassembler with the specified binary file.

# Ensure the correct number of arguments are provided
if [ "$#" -ne 1 ]; then
    echo "Usage: ./run.sh <binary_code_filename>"
    exit 1
fi

# Run the Python disassembler with the given filename
python3 disassembler.py "$1"