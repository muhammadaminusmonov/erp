# Base image
FROM python:3.10-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set work directory
WORKDIR /code

# Install dependencies
COPY requirements.txt .
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# Copy project
COPY . .

# Collect static files (if needed)
RUN python src/manage.py collectstatic --noinput --clear

# Run Gunicorn (correct path based on your structure)
CMD ["gunicorn", "src.erp.wsgi:application", "--bind", "0.0.0.0:8000"]