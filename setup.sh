#! /usr/bin/env bash

# Install python packages
pip install -r requirements.txt -t vendored

# Setup api keys
echo -e "Now run:\nsource secrets/api_keys_DO_NOT_RENAME"
