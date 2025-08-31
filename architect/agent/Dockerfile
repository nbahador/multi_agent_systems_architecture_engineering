# =============================================================================
# DOCKERFILE TEMPLATE - Python Application
# =============================================================================
# This template helps you containerize any Python application
# Follow the comments to customize for your specific project

# -----------------------------------------------------------------------------
# 1. BASE IMAGE SELECTION
# -----------------------------------------------------------------------------
# Choose your Python version based on your project requirements
# Common options:
#   - python:3.12-slim (latest, smaller size)
#   - python:3.11-slim (stable, widely supported)
#   - python:3.10-slim (older but very stable)
#   - python:3.12 (full version with more tools, larger size)

FROM python:3.12-slim
# ↑ CUSTOMIZE: Replace with your preferred Python version

# -----------------------------------------------------------------------------
# 2. WORKING DIRECTORY SETUP
# -----------------------------------------------------------------------------
# Sets where your application will live inside the container
# Standard practice is /app, but you can change it

WORKDIR /app
# ↑ CUSTOMIZE: Change to your preferred directory (e.g., /myapp, /src)

# -----------------------------------------------------------------------------
# 3. DEPENDENCY INSTALLATION
# -----------------------------------------------------------------------------
# Copy requirements file first for better Docker layer caching
# This means dependencies only reinstall when requirements.txt changes

COPY requirements.txt /app/requirements.txt
# ↑ CUSTOMIZE: Replace 'requirements.txt' with your dependency file name
#              Options: requirements.txt, pyproject.toml, Pipfile, etc.

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt
# ↑ CUSTOMIZE: Modify installation command based on your setup:
#              - For pip: pip install --no-cache-dir -r requirements.txt
#              - For poetry: pip install poetry && poetry install --no-dev
#              - For pipenv: pip install pipenv && pipenv install --system

# -----------------------------------------------------------------------------
# 4. APPLICATION CODE COPY
# -----------------------------------------------------------------------------
# Copy your entire application code to the container
# The '.' means "copy everything from current directory"

COPY . /app
# ↑ CUSTOMIZE: Modify source and destination as needed:
#              - COPY ./src /app (if code is in 'src' folder)
#              - COPY ./myproject /app (if code is in specific folder)
#              - COPY *.py /app (if you only want Python files)

# -----------------------------------------------------------------------------
# 5. ENVIRONMENT VARIABLES
# -----------------------------------------------------------------------------
# Set environment variables for your application
# PYTHONPATH tells Python where to find your modules

ENV PYTHONPATH=/app
# ↑ CUSTOMIZE: Add any environment variab
