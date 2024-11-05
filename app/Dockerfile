# Base image
FROM python:3.10-alpine

# Install poetry
RUN pip install poetry

# Set working directory
WORKDIR /app

# Copy dependency files
COPY pyproject.toml poetry.lock /app/

# Project initialization - add --no-root to avoid copying source code
RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi --no-root

# Copy the rest of the application
COPY . /app/

# Install project with poetry
RUN poetry install --no-interaction --no-ansi

# Expose port
EXPOSE 5000

# Use direct command instead of poetry run
CMD ["python", "app.py"]