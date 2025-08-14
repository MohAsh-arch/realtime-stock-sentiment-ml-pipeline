#!/bin/bash

set -e  # stop script if any command fails

python3 -m ensurepip --upgrade
python3 -m pip install --upgrade pip

pip install pandas numpy requests
pip install flask
pip install apache-airflow
pip install psycopg2-binary
pip install python-dotenv

echo "✅ All packages installed successfully!"
