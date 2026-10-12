#!/bin/bash
#usage: fsa_acceptor.sh <fsa_filename> <input_filename> <output_filename>
python3 "$(dirname "$0")/fsa_acceptor.py" "$@"