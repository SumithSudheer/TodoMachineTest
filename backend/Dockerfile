# Use lightweight Python image
FROM python:3.12-slim

# Set working directory inside container
WORKDIR /app

# Copy dependency list first (for layer caching)
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . .

# Ensure media directory exists
RUN mkdir -p /app/media

# Expose Django's port
EXPOSE 8000

# Default command (can be changed to gunicorn in prod)
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
