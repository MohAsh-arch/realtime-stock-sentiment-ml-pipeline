FROM apache/airflow:2.9.0

USER root

# System deps
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Switch to airflow working dir
WORKDIR /opt/airflow/app

# Copy requirements
COPY pyproject.toml ./
COPY docker/requirements_airflow.txt ./requirements_airflow.txt

# Install pip packages as airflow user (not root)
USER airflow
RUN pip install --no-cache-dir --upgrade pip \
    && if [ -f requirements_airflow.txt ]; then pip install --no-cache-dir -r requirements_airflow.txt; fi

# Back to default
USER airflow
