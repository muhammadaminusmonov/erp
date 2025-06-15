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

# 4) Use /code/src as the working dir for gunicorn
WORKDIR /code/src

# Run Gunicorn (correct path based on your structure)
CMD ["gunicorn", "erp.wsgi:application", "--bind", "0.0.0.0:8000"]