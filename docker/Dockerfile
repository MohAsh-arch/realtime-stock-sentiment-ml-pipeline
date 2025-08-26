# Base image
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Install OS dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    curl \
    nano \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements script into container
COPY docker/requirements.sh .

# Make script executable & run it
RUN chmod +x requirements.sh && ./requirements.sh

# Default command (keep container alive for dev)
CMD ["bash"]
