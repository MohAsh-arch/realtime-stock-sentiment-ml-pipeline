#!/bin/bash

set -e  # stop script if any command fails

python3 -m ensurepip --upgrade
python3 -m pip install --upgrade pip

pip install pandas numpy requests  pytest 
pip install --no-cache-dir python-dotenv

pip install psycopg2-binary sqlalchemy


echo "All packages installed successfully!"
