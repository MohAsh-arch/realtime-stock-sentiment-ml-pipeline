#!/bin/bash

set -e  # stop script if any command fails

python3 -m ensurepip --upgrade
python3 -m pip install --upgrade pip

pip install pandas numpy requests pyspark pytest


echo "All packages installed successfully!"
