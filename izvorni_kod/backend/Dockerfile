# Backend Dockerfile
FROM python:3.11-slim

WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir --upgrade pip && \
   pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Expose port
EXPOSE 5000

# Set PYTHONPATH to include src directory
ENV PYTHONPATH=/app/src:${PYTHONPATH}

# Run the application
CMD ["python", "run.py"]
